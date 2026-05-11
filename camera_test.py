from ultralytics import YOLO

# 1. 載入你訓練好的模型
model = YOLO(r"runs\detect\train4\weights\best.pt")

# 2. 開啟攝影機即時辨識
model.predict(
    source=0,      # 0 = webcam
    show=True,     # 顯示畫面
    conf=0.5       # 信心門檻（可調）
)