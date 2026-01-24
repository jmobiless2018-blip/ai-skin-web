from flask import Flask, render_template, request
import os
import random

app = Flask(__name__)

# โฟลเดอร์เก็บไฟล์อัปโหลด
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------------
# ✅ หน้าแรก
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------------
# ✅ วิเคราะห์ + แสดงผล
# -------------------------------
@app.route("/result", methods=["POST"])
def result():
    file = request.files["image"]

    # เซฟไฟล์รูป
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # ✅ ตัวอย่างประเภทผื่น (เพิ่มได้)
    rash_list = [
        {"name": "ผื่นภูมิแพ้ผิวหนัง", "advice": "หลีกเลี่ยงสารกระตุ้น และทาครีมบำรุง"},
        {"name": "ผดร้อน", "advice": "พักในที่เย็น หลีกเลี่ยงเหงื่อสะสม"},
        {"name": "ผื่นเชื้อรา", "advice": "รักษาความสะอาดและพบแพทย์หากลุกลาม"},
        {"name": "สิวอักเสบ", "advice": "หลีกเลี่ยงการบีบสิว และใช้ยาตามแพทย์แนะนำ"},
        {"name": "ลมพิษ", "advice": "หลีกเลี่ยงอาหารหรือสิ่งกระตุ้น และพบแพทย์หากรุนแรง"},
    ]

    # ✅ สุ่มผลลัพธ์ให้เหมือน AI
    random.shuffle(rash_list)

    results = []
    confidence = 90

    for r in rash_list[:4]:
        results.append({
            "name": r["name"],
            "confidence": confidence
        })
        confidence -= random.randint(10, 20)

    main_rash = {
        "name": rash_list[0]["name"],
        "confidence": results[0]["confidence"],
        "advice": rash_list[0]["advice"]
    }

    return render_template(
        "result.html",
        filename="uploads/" + filename,
        main_rash=main_rash,
        results=results
    )


# -------------------------------
# ✅ Run Local
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
