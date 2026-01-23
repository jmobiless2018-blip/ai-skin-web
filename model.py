from PIL import Image
import numpy as np

def predict_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    arr = np.array(img)

    # วิเคราะห์สีแดง (ผื่นมักแดง)
    red_channel = arr[:, :, 0]
    redness = np.mean(red_channel) / 255  # 0–1

    # วิเคราะห์ความหยาบของภาพ (texture)
    gray = np.mean(arr, axis=2)
    texture = np.std(gray) / 128  # ปรับให้อยู่ช่วงใกล้ 0–1

    # รวมคะแนน
    score = (0.6 * redness) + (0.4 * texture)

    # แปลงเป็นเปอร์เซ็นต์ (กำหนดช่วง 65–95%)
    confidence = int(65 + score * 30)
    confidence = max(65, min(confidence, 95))

    # กำหนดชนิดผื่น (ตัวอย่าง rule-based)
    if redness > 0.6:
        disease = "ผื่นภูมิแพ้ผิวหนัง"
        advice = "หลีกเลี่ยงสารกระตุ้น และพบแพทย์หากอาการไม่ดีขึ้น"
    elif redness > 0.45:
        disease = "ผดร้อน"
        advice = "หลีกเลี่ยงความร้อน รักษาความแห้งของผิว"
    else:
        disease = "ผื่นแพ้"
        advice = "สังเกตอาการและหลีกเลี่ยงสารที่อาจก่อให้เกิดการแพ้"

    return disease, confidence, advice
