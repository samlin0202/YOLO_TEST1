from flask import Flask, request, jsonify

app = Flask(__name__)

# =========================
# 📊 全域資料（統計用）
# =========================
data_log = []

count = {
    "bottle": 0,
    "can": 0
}

# =========================
# 🏠 首頁（避免 404）
# =========================
@app.route("/")
def home():
    return """
    <h1>YOLO Detection Server</h1>
    <p>Server is running successfully 🚀</p>
    <p>Available API:</p>
    <ul>
        <li>/upload (POST)</li>
        <li>/stats (GET)</li>
        <li>/data (GET)</li>
    </ul>
    """

# =========================
# 📡 接收 YOLO 上傳資料
# =========================
@app.route("/upload", methods=["POST"])
def upload():
    data = request.json

    # 存原始資料
    data_log.append(data)

    obj = data.get("class")

    # 統計數量
    if obj in count:
        count[obj] += 1

    print("📩 Received:", data)

    return jsonify({
        "status": "ok",
        "message": "data received"
    })

# =========================
# 📊 回傳統計結果（圖表用）
# =========================
@app.route("/stats")
def stats():
    return jsonify(count)

# =========================
# 📦 回傳所有資料紀錄
# =========================
@app.route("/data")
def data():
    return jsonify(data_log)

# =========================
# 🚀 啟動 server
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )