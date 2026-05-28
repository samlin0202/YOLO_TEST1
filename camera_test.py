from ultralytics import YOLO
import cv2

model = YOLO(r"runs\detect\train4\weights\best.pt")

cap = cv2.VideoCapture(0)

TARGETS = ["bottle", "can"]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.5)

    annotated_frame = results[0].plot()

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            name = model.names[cls_id]

            if name in TARGETS:
                print("🚨 Detected:", name)

    cv2.imshow("YOLO", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()