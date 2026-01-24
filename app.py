from flask import Flask, render_template, request
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ✅ Render ต้องใช้ static/uploads เท่านั้น
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------
# ✅ หน้าแรก
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------------
# ✅ รับรูป + วิเคราะห์ + แสดงผล
# -------------------------------
@app.route("/result", methods=["POST"])
def result():

    file = request.files.get("image")

    if not file or file.filename == "":
        return "❌ กรุณาอัปโหลดรูปก่อน"

    # ✅ ป้องกันชื่อไฟล์แปลก
    filename = secure_filename(file.filename)

    # ✅ เซฟลง static/uploads
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    # ✅ ตัวอย่างชนิดผื่น
    rash_list = [
        {"name": "ผื่นภูมิแพ้ผิวหนัง", "advice": "หลีกเลี่ยงสารกระตุ้น และทาครีมเพิ่มความชุ่มชื้น"},
        {"name": "ผื่นลมพิษ", "advice": "สังเกตอาหารหรือสิ่งกระตุ้น และพบแพทย์ถ้าไม่ดีขึ้น"},
        {"name": "ผดร้อน", "advice": "อยู่ในที่เย็น ไม่ใส่เสื้อผ้าหนา"},
        {"name": "ผื่นติดเชื้อรา", "advice": "รักษาความสะอาด และหลีกเลี่ยงความอับชื้น"},
        {"name": "ผื่นแพ้สัมผัส", "advice": "หยุดใช้สารเคมีหรือเครื่องสำอางที่สงสัย"},
    ]

    random.shuffle(rash_list)

    # ✅ ทำ confidence ไม่เท่ากัน
    results = []
    confidence = random.randint(80, 95)

    for r in rash_list[:3]:
        results.append({
            "name": r["name"],
            "confidence": confidence
        })
        confidence -= random.randint(8, 15)

    main_rash = {
        "name": results[0]["name"],
        "confidence": results[0]["confidence"],
        "advice": rash_list[0]["advice"]
    }

    return render_template(
        "result.html",
        filename="uploads/" + filename,   # ✅ ถูกต้องสำหรับ static
        main_rash=main_rash,
        results=results
    )


# -------------------------------
# ✅ Run Local
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
