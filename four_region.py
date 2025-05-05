import cv2
import torch

# Load YOLOv5 model
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)

# Set device
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device).eval()

# Simulated region status
regions = {
    "Region 1": False,
    "Region 2": False,
    "Region 3": False,
    "Region 4": False
}

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

    # Divide the frame into four equal-sized regions
    region_width = width // 2
    region_height = height // 2

    # Draw regions and numbers
    cv2.rectangle(frame, (0, 0), (region_width, region_height), (255, 0, 0), 2)
    cv2.putText(frame, "Region 1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.rectangle(frame, (region_width, 0), (width, region_height), (0, 255, 0), 2)
    cv2.putText(frame, "Region 2", (width - 140, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.rectangle(frame, (0, region_height), (region_width, height), (0, 0, 255), 2)
    cv2.putText(frame, "Region 3", (10, height // 2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.rectangle(frame, (region_width, region_height), (width, height), (255, 255, 0), 2)
    cv2.putText(frame, "Region 4", (width - 140, height // 2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

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
            y_center = (ymin + ymax) // 2

            if x_center < region_width and y_center < region_height:
                regions["Region 1"] = True
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 2)
            elif x_center >= region_width and y_center < region_height:
                regions["Region 2"] = True
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
            elif x_center < region_width and y_center >= region_height:
                regions["Region 3"] = True
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 0, 255), 2)
            elif x_center >= region_width and y_center >= region_height:
                regions["Region 4"] = True
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 255, 0), 2)

    # Display region status directly inside the corresponding region
    for region, status in regions.items():
        text = "ON" if status else "OFF"
        region_num = int(region[-1])
        if region_num == 1:
            cv2.putText(frame, text, (10, region_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if status else (0, 0, 255), 2)
        elif region_num == 2:
            cv2.putText(frame, text, (width - 140, region_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if status else (0, 0, 255), 2)
        elif region_num == 3:
            cv2.putText(frame, text, (10, height // 2 + 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if status else (0, 0, 255), 2)
        elif region_num == 4:
            cv2.putText(frame, text, (width - 140, height // 2 + 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if status else (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close the window
cap.release()
cv2.destroyAllWindows()