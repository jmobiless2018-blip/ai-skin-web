from flask import Flask, render_template, request
import os, random

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ หน้าแรก
@app.route("/")
def home():
    return render_template("index.html")


# ✅ ต้อง POST เท่านั้น
@app.route("/result", methods=["POST"])
def result():

    if "image" not in request.files:
        return "❌ ไม่พบไฟล์"

    file = request.files["image"]

    if file.filename == "":
        return "❌ ไม่ได้เลือกไฟล์"

    filename = file.filename

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # ✅ ตัวอย่างผลลัพธ์
    rash_list = [
        {"name": "ผื่นภูมิแพ้ผิวหนัง", "advice": "หลีกเลี่ยงสารกระตุ้น"},
        {"name": "ผดร้อน", "advice": "อยู่ในที่เย็น ลดเหงื่อ"},
        {"name": "เชื้อราผิวหนัง", "advice": "รักษาความสะอาด"},
        {"name": "ผื่นแพ้สัมผัส", "advice": "หยุดใช้สารที่แพ้"},
    ]

    random.shuffle(rash_list)

    confidence = 90
    results = []

    for r in rash_list:
        results.append({
            "name": r["name"],
            "confidence": confidence
        })
        confidence -= random.randint(10, 20)

    main_rash = {
        "name": results[0]["name"],
        "confidence": results[0]["confidence"],
        "advice": rash_list[0]["advice"]
    }

    return render_template(
        "result.html",
        filename="uploads/" + filename,
        main_rash=main_rash,
        results=results
    )


if __name__ == "__main__":
    app.run()
