import cv2
import torch
import time
import serial

# Load YOLOv5 model
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)

# Set device
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device).eval()

# Simulated region status
regions = {
    "Left Region": False,
    "Right Region": False
}

# Last time a human was detected in each region
last_human_time = {
    "Left Region": 0,
    "Right Region": 0
}

# Function to update region status and send commands to Arduino
def update_regions():
    current_time = time.time()
    for region, status in regions.items():
        if status:
            last_human_time[region] = current_time
            if region == "Left Region":
                arduino.write(b'1')  # Send command '1' to turn on left LED
            else:
                arduino.write(b'2')  # Send command '2' to turn on right LED
        else:
            time_since_last_human = current_time - last_human_time[region]
            if time_since_last_human > 5:  # Turn off LED after 5 seconds
                if region == "Left Region":
                    arduino.write(b'3')  # Send command '3' to turn off left LED
                else:
                    arduino.write(b'4')  # Send command '4' to turn off right LED

# Open serial communication with Arduino
arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with the appropriate port

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Failed to open webcam")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame")
        break

    # Flip the frame horizontally to correct mirroring
    frame = cv2.flip(frame, 1)

    # Get dimensions of the frame
    height, width, _ = frame.shape

    # Divide the frame into two equal-sized regions vertically
    region_width = width // 2

    # Draw regions and labels
    cv2.rectangle(frame, (0, 0), (region_width, height), (255, 0, 0), 2)
    cv2.putText(frame, "Left Region", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.rectangle(frame, (region_width, 0), (width, height), (0, 255, 0), 2)
    cv2.putText(frame, "Right Region", (width - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Perform YOLOv5 inference on the frame
    results = model(frame)

    # Reset region status
    for region in regions:
        regions[region] = False

    # Check if humans are detected in each region and draw squares around them
    for detection in results.xyxy[0]:
        if detection[5] == 0:  # Class index 0 corresponds to humans in YOLOv5
            xmin, ymin, xmax, ymax, confidence = detection[:5].cpu().numpy()
            x_center = (xmin + xmax) // 2

            if x_center < region_width:
                regions["Left Region"] = True
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 2)
            else:
                regions["Right Region"] = True
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)

    # Update region status and send commands to Arduino
    update_regions()

    # Display region status directly on the frame
    text_left = "ON" if regions["Left Region"] else "OFF"
    text_right = "ON" if regions["Right Region"] else "OFF"
    cv2.putText(frame, f"Left Region: {text_left}", (10, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0) if regions["Left Region"] else (0, 0, 255), 2)
    cv2.putText(frame, f"Right Region: {text_right}", (width - 250, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0) if regions["Right Region"] else (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close the window
cap.release()
cv2.destroyAllWindows()