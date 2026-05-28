from ultralytics import YOLO
import cv2
import time
import os
import requests

# =========================
# 🤖 載入模型
# =========================
model = YOLO(r"runs\detect\train4\weights\best.pt")

cap = cv2.VideoCapture(0)

TARGETS = ["bottle", "can"]

save_dir = "captures"
os.makedirs(save_dir, exist_ok=True)

last_capture_time = 0
cooldown = 3

# =========================
# 🔁 主迴圈
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera error")
        break

    results = model(frame, conf=0.5)
    annotated = results[0].plot()

    detected_this_frame = False

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            name = model.names[cls_id]
            conf = float(box.conf[0])

            if name in TARGETS:
                detected_this_frame = True
                print(f"🚨 Detected: {name} ({conf:.2f})")

                now = time.time()

                # =========================
                # 📸 拍照 + HTTP
                # =========================
                if now - last_capture_time > cooldown:

                    filename = f"{save_dir}/{name}_{int(now)}.jpg"
                    cv2.imwrite(filename, frame)

                    print(f"📸 Saved: {filename}")

                    # =========================
                    # 📡 HTTP 上傳（重點修正）
                    # =========================
                    try:
                        response = requests.post(
                            "http://127.0.0.1:5000/upload",
                            json={
                                "class": name,
                                "confidence": conf,
                                "image": filename
                            },
                            timeout=3
                        )

                        print("📡 Upload status:", response.status_code)
                        print("📡 Response:", response.text)

                        print("📡 Uploaded to server")

                    except Exception as e:
                        print("❌ Upload failed:", e)

                    last_capture_time = now

    if not detected_this_frame:
        print("...")  # 沒偵測到就不刷太多

    cv2.imshow("YOLO Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()