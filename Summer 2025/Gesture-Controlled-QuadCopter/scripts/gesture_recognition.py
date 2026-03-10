import cv2
import mediapipe as mp
import numpy as np
import math
import joblib
from itertools import combinations
import os
import time
import warnings
import threading

warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

class GestureRecognizer:
    def __init__(self, model_dir='D:/Media/Model', camera_index=0, show_window=False):  # Put the path of your model file: 
        self.model_dir = model_dir
        self.camera_index = camera_index
        self.show_window = show_window
        self.current_gesture = "Initializing..."
        self.is_running = False
        self.user_palm_size = None
        self.last_update_time = time.time()
        self.latest_frame = None
        self.latest_landmarks = None
        self.lock = threading.Lock()
        self.thread = None
        try:
            self._load_models()
            self._initialize_mediapipe()
            self._initialize_camera()
            self._calibrate()
        except Exception as e:
            print(f"Critical error during initialization: {e}")
            if hasattr(self, 'cap') and self.cap.isOpened():
                self.cap.release()
            raise

    def _load_models(self):
        print("Loading models...")
        self.model = joblib.load(os.path.join(self.model_dir, 'gesture_model.pkl')) #path of your pkl files of the model. 
        self.scaler = joblib.load(os.path.join(self.model_dir, 'gesture_scaler.pkl'))
        self.label_encoder = joblib.load(os.path.join(self.model_dir, 'gesture_label_encoder.pkl'))
        self.threshold = joblib.load(os.path.join(self.model_dir, 'gesture_conf_threshold.pkl'))
        print("Models loaded successfully.")

    def _initialize_mediapipe(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

    def _initialize_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise IOError(f"Cannot open camera at index {self.camera_index}")

    def _calibrate(self, duration=5.0): # can change the caliberation time.
        calibration_path = 'user_calibration.pkl'
        if os.path.exists(calibration_path):
            self.user_palm_size = joblib.load(calibration_path)
            print(f"Loaded saved calibration. Palm size: {self.user_palm_size:.5f}")
            return
        print("Calibration: Place your hand flat in front of the camera.")
        print(f"Hold still for about {duration} seconds...")
        start_time = time.time()
        palm_sizes = []
        while time.time() - start_time < duration:
            success, frame = self.cap.read()
            if not success: continue
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)
            display_text = "Calibrating..." if result.multi_hand_landmarks else "Show your hand!"
            color = (0, 255, 255) if result.multi_hand_landmarks else (0, 0, 255)
            if result.multi_hand_landmarks:
                points = [(lm.x, lm.y, lm.z) for lm in result.multi_hand_landmarks[0].landmark]
                p1, p2 = points[5], points[17]
                palm_size = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)
                palm_sizes.append(palm_size)
            cv2.putText(frame, display_text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
            cv2.imshow("Calibration", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyWindow("Calibration")
        if len(palm_sizes) < 10:
            print("Calibration failed. Not enough stable frames. Please try again.")
            self.cap.release()
            exit()
        self.user_palm_size = float(np.mean(palm_sizes))
        print(f"Calibration complete. Avg palm size = {self.user_palm_size:.5f}")
        joblib.dump(self.user_palm_size, calibration_path)

    def _recognition_loop(self):
        while self.is_running:
            success, frame = self.cap.read()
            if not success:
                time.sleep(0.1)
                continue
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)
            gesture = None
            landmarks = None
            if result.multi_hand_landmarks:
                landmarks = result.multi_hand_landmarks[0]
                points = [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]
                features = []
                for i, j in combinations(range(21), 2):
                    p1, p2 = points[i], points[j]
                    dist = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
                    features.append(dist / self.user_palm_size)
                X_live_scaled = self.scaler.transform(np.array(features).reshape(1, -1))
                pred_proba = self.model.predict_proba(X_live_scaled)[0]
                max_prob = np.max(pred_proba)
                if max_prob >= self.threshold:
                    pred_class_idx = np.argmax(pred_proba)
                    gesture = self.label_encoder.inverse_transform([pred_class_idx])[0]
                else:
                    gesture = "Unknown"
            with self.lock:
                self.current_gesture = gesture
                self.last_update_time = time.time()
                self.latest_frame = frame.copy()
                self.latest_landmarks = landmarks
            if self.show_window:
                display_text = gesture if gesture else "No Hand"
                cv2.putText(frame, display_text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                if landmarks:
                    self.mp_draw.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)
                cv2.imshow("Gesture Recognizer (Debug)", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.is_running = False
        self.cap.release()
        cv2.destroyAllWindows()
        print("Gesture detection stopped")

    def start(self):
        if self.is_running:
            print("Gesture recognition is already running.")
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._recognition_loop, daemon=True)
        self.thread.start()
        print("Gesture recognition thread started.")

    def stop(self):
        if not self.is_running:
            return
        print("Stopping gesture recognition thread...")
        self.is_running = False
        if hasattr(self, 'cap') and self.cap.isOpened():
            print("Releasing camera capture...")
            self.cap.release()
        if self.thread:
            print("Joining gesture thread...")
            self.thread.join()
            print("Gesture thread joined.")

    def get_latest_data(self):
        with self.lock:
            return self.current_gesture, self.last_update_time
    
    def get_visual_data(self):
        with self.lock:
            return self.latest_frame, self.latest_landmarks

#Testing block: 
#Will not run in the main script when imported.
if __name__ == '__main__':
    print("Test Runnnnnnn")
    recognizer = GestureRecognizer(show_window=True)
    recognizer.start()

    try:
        while True:
            gesture, timestamp = recognizer.get_latest_data()
            if gesture:
                print(f"Detected Gesture: {gesture} (Updated {time.time() - timestamp:.2f}s ago)")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        recognizer.stop()