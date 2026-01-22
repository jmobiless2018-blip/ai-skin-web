from flask import Flask, render_template, request
import os
from model import predict_image

# ✅ ต้องอยู่ก่อน route เสมอ
app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    filename = file.filename

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    disease, confidence, advice = predict_image(filepath)

    return render_template(
        "result.html",
        filename=filename,
        disease=disease,
        confidence=confidence,
        advice=advice
    )


# ✅ ต้องมีเสมอ
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

