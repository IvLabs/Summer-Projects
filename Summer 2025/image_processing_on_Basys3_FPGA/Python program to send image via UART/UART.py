import cv2
import serial

# --- Step 1: Choose image file ---
file_path = "C:\My Drive\iv labs\images\iron.jpg"

img = cv2.imread(file_path)
if not file_path:
    print("No image selected. Exiting.")   
    exit() 

# --- Step 2: Load and resize image ---
height = 240
width = 320


if img is None:
    print("Error: Could not load image.")
    exit()

img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
print(img.shape)
resized = cv2.resize(img, (width, height))
print(resized.shape)

# --- Step 3: Open serial port ---
try:
    uart = serial.Serial(port='COM5', baudrate=115200)
    print("Connected to COM8")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()

# --- Step 4: Send pixel data over UART ---
print(f"Sending {width}x{height} pixels...")
for row in resized:
    for pixel in row:
        r, b, g = pixel
        uart.write(bytes([r, b, g]))
        print(pixel)



uart.close()
print("Done. Serial port closed.") 