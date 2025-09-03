"""
Real-time YOLO (ultralytics) webcam demo:
- Detects 'person' and 'cell phone'
- Computes bounding box center
- Determines if center is in LEFT or RIGHT half of the frame
- Prints results to console and overlays info on the feed
Press 'q' to quit.
"""

import cv2
from ultralytics import YOLO
import time

# Choose which pretrained weights to use:
MODEL_WEIGHTS = "yolov8n.pt"

def main(camera_index=0, conf_thres=0.3, imgsz=640):
    # Load model
    model = YOLO(MODEL_WEIGHTS)

    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam. Try a different camera index.")
        return

    prev_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to read frame from camera.")
            break

        frame_height, frame_width = frame.shape[:2]
        mid_x = frame_width / 2.0

        # Run YOLO prediction on a single frame.
        # conf=conf_thres sets the confidence threshold.
        # imgsz favors speed/accuracy tradeoff.
        results = model(frame, conf=conf_thres, imgsz=imgsz)

        if len(results) > 0:
            r = results[0]

            # r.boxes contains detection boxes. Each box has:
            # - xyxy coordinates (x1, y1, x2, y2)
            # - cls (class id)
            # - conf (confidence)
            # names mapping is in r.names
            for i, box in enumerate(r.boxes):
                try:
                    # Extract xyxy as Python floats
                    xyxy = box.xyxy[0].cpu().numpy() if hasattr(box.xyxy[0], "cpu") else box.xyxy[0].numpy()
                    x1, y1, x2, y2 = map(float, xyxy)
                except Exception:
                    # Fallback if the structure is slightly different
                    x1, y1, x2, y2 = map(float, box.xyxy[0])

                # class id and name
                try:
                    cls_id = int(box.cls[0].cpu().numpy()) if hasattr(box.cls[0], "cpu") else int(box.cls[0].numpy())
                except Exception:
                    cls_id = int(box.cls[0])

                class_name = r.names.get(cls_id, str(cls_id))

                # Filter only person or cell phone (names: 'person', 'cell phone')
                if class_name.lower() in ("person", "cell phone", "cellphone", "mobile phone", "cell_phone"):
                    # center point
                    cx = (x1 + x2) / 2.0
                    cy = (y1 + y2) / 2.0

                    # Decide left or right half
                    if cx < mid_x:
                        side = "LEFT"
                    elif cx > mid_x:
                        side = "RIGHT"
                    else:
                        side = "CENTER"

                    # Draw bounding box and center
                    x1_i, y1_i, x2_i, y2_i = map(int, (x1, y1, x2, y2))
                    cx_i, cy_i = int(cx), int(cy)

                    # Color: green box, blue center dot (OpenCV BGR)
                    cv2.rectangle(frame, (x1_i, y1_i), (x2_i, y2_i), (0, 255, 0), 2)
                    cv2.circle(frame, (cx_i, cy_i), 4, (255, 0, 0), -1)

                    # Overlay label with side and confidence
                    conf_score = float(box.conf[0]) if hasattr(box, "conf") else None
                    label = f"{class_name} {side}"
                    if conf_score is not None:
                        label += f" {conf_score:.2f}"

                    # put label above box
                    cv2.putText(frame, label, (x1_i, max(20, y1_i - 6)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # Print to console (real-time)
                    print(f"[{time.strftime('%H:%M:%S')}] Detected {class_name} at center ({cx_i},{cy_i}) -> {side}")

        # draw center vertical line
        cv2.line(frame, (int(mid_x), 0), (int(mid_x), frame_height), (0, 0, 255), 1)

        # FPS overlay
        now = time.time()
        fps = 1.0 / (now - prev_time) if (now - prev_time) > 0 else 0.0
        prev_time = now
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Show frame
        cv2.imshow("YOLO Range-awareness Demo - Press 'q' to quit", frame)

        # quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
