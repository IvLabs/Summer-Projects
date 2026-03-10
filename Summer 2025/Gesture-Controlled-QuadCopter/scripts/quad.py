from __future__ import print_function
import time
import cv2
from dronekit import connect, VehicleMode
from pymavlink import mavutil
from collections import deque, Counter

# Import our gesture recognisation...
# Our Gestures Model is trained in Windows Os so it will not work in other OS
from gesture_recognition import GestureRecognizer

# Connection with the drone is done here:
#connectin string protocol:ip:port
connection_string = 'udp:0.0.0.0:14551' 
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)  #timeout is changed to 60s form default
print("Drone connected")

# The is the function that encodes velocity msg and sends the packet using dronekit
# All the paraments are listed 
def send_ned_velocity(velocity_x, velocity_y, velocity_z):
    """Send velocity command to the drone in a body-fixed frame."""
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # Frame relative to drone's body
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z,
        0, 0, 0, # x, y, z acceleration (not used)
        0, 0)    # yaw, yaw_rate (not used)
    vehicle.send_mavlink(msg)
    vehicle.flush()

def gesture_to_velocity(gesture):
    speed = 0.5 # m/s
    if gesture == "takeoff":
        return (0, 0, -speed)  # Throttle Up. Downward is positive.
    elif gesture == "land":
        return (0, 0, 0)      # Hover
    elif gesture == "pitch_forward":
        return (speed, 0, 0)  # Move forward
    elif gesture == "pitch_backward":
        return (-speed, 0, 0) # Move backward
    elif gesture == "roll_right":
        return (0, speed, 0)  # Move right
    elif gesture == "roll_left":
        return (0, -speed, 0) # Move left
    else:
        return (0, 0, 0)   

recognizer = GestureRecognizer(show_window=False) 
recognizer.start() # Start and Calibberation for user's hand. 
print("Gesture recognizer starting...")
time.sleep(0.5)
print("Ready to Start...")

#Start of the program
try:
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    
    while(vehicle.mode != VehicleMode("GUIDED")):  #Safety: Script will not proceed until it is armed and set to guided with RC or mavproxy
        print("waitihng for Mode: Guided ")
        time.sleep(1)
    


    takeoff_alt = 3
    print(f"Taking off to {takeoff_alt} meters...")
    vehicle.simple_takeoff(takeoff_alt)  #Velocity script is not function untill the vehicle is not in air. 
    
    while True:
        alt = vehicle.location.global_relative_frame.alt    #Height is relative here: measured form there it took a takeoff
        print(" Altitude: ", alt)
        if alt >= 0.95 * takeoff_alt:
            print("Target altitude reached")
            time.sleep(5)  # Wait time for it stabilize
            break
        time.sleep(0.5)

    # Drone movements command forwarding loop
    print("Control loop started. Press 'ESC' in the video window to exit.")
    
    stable_gest = None
    prev_stable_gest = None
    land_timer_start = None

    gesture_buffer = deque(maxlen=15) # A queue of 15 to eliminate any errors to make transition smooth. Can change the size.
    STABILITY_THRESHOLD = 0.7 # Gestures are sent only whem 70% in the queue are of same type. +- to get your optimal transition. 
    
    while True:
        current_gest, timestamp = recognizer.get_latest_data()
        gesture_buffer.append(current_gest)

        if len(gesture_buffer) == gesture_buffer.maxlen:
            most_common = Counter(gesture_buffer).most_common(1)[0]
            most_common_gesture, count = most_common
            
            if most_common_gesture is not None and count >= (gesture_buffer.maxlen * STABILITY_THRESHOLD):
                stable_gest = most_common_gesture
            else:
                stable_gest = None 

        # If there is no gesture data for 2 seconds then it will hover to safety..
        if time.time() - timestamp > 2.0:
            print("WARNING: Gestures error ! Hovering for safety.")
            send_ned_velocity(0, 0, 0) # Sending zero velocity message.
            stable_gest = None 

        # when gesture changes. the transitiion to stop then move to new movement command or look for landing countdown.
        if stable_gest != prev_stable_gest:
            print(f"New stable gesture: {stable_gest if stable_gest else 'None'}")
            send_ned_velocity(0, 0, 0) # Stop during transition
            time.sleep(0.2)
            prev_stable_gest = stable_gest

            if stable_gest == "land":
                print("Stable 'Land' detected. Starting 5-second land timer.")
                land_timer_start = time.time()
            else:
                land_timer_start = None # timer resets if land changes in that 5 seconds. 
        
        # Safe landing action to prevent any sudden landing if landing is detected my users mistake. 
        if stable_gest == "land" and land_timer_start is not None:
            if time.time() - land_timer_start > 5.0:
                print(" 'Land' held for 5 seconds. Initiating LAND mode...")
                vehicle.mode = VehicleMode("LAND")
                land_timer_start = None # Reset timer to avoid re triggering
                time.sleep(2) # Time to start landing
                break # Exit the loop..

        # Send continuous stream of command messages to keep drone in motion is gesture is held. 
        if vehicle.mode == VehicleMode("GUIDED"):
            vx, vy, vz = gesture_to_velocity(stable_gest)
            send_ned_velocity(vx, vy, vz)

        # Window to view the camera feed. 
        frame, landmarks = recognizer.get_visual_data()
        if frame is not None:
            if landmarks:
                for idx, lm in enumerate(landmarks.landmark):
                    h, w, _ = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)
            
            display_text = stable_gest if stable_gest is not None else "No Stable Gesture"
            cv2.putText(frame, f"Gesture: {display_text}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
            cv2.imshow('Gesture Control Feed', frame)
        #if frame is not None:
            #display_text = stable_gest if stable_gest else "..."
            #cv2.putText(frame, f"Stable Gesture: {display_text}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
            #cv2.imshow('Drone Gesture Control', frame)
            # If you dont want skeletal representation then activate this part and deactiveate other one.
            
            if cv2.waitKey(1) & 0xFF == 27: 
                print("ESC key pressed. Exiting...")
                break
        
        time.sleep(0.1)  

finally:
    # After command loop exit a land. The shutdown of the script.
    print("Shutting down...")
    print("Setting vehicle to LAND mode for safety.")
    vehicle.mode = VehicleMode("LAND")
    recognizer.stop()
    cv2.destroyAllWindows()
    vehicle.close()
    print("Shutdown complete.")
