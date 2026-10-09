import cv2
import numpy as np
import os

def analyze_bone_image(image_path):
    """
    وظيفة هذا السكربت: استقبال صورة العظم، معالجتها، استخراج الحواف، 
    وحساب القياسات الأولية لمساعدة الخبير الطبي.
    """
    if not os.path.exists(image_path):
        print(f"خطأ: صورة العظم غير موجودة في المسار: {image_path}")
        return None

    # 1. قراءة الصورة
    image = cv2.imread(image_path)

    # 2. تحويل الصورة إلى تدرج الرمادي (Grayscale) لتسهيل التحليل الرياضي
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. تطبيق فلتر لتقليل التشويش (Gaussian Blur)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. خوارزمية Canny لاكتشاف الحواف والحدود (Edge Detection) لمعرفة أبعاد العظم وطوله
    edges = cv2.Canny(blurred, 50, 150)

    # 5. العثور على الخطوط أو الحدود الخارجية للعظم
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # العثور على أكبر محيط (والذي يمثل عظمة الهيكل غالباً)
        largest_contour = max(contours, key=cv2.contourArea)

        # حساب صندوق الإحاطة (Bounding Box) لمعرفة الطول والعرض بالبكسل
        x, y, w, h = cv2.boundingRect(largest_contour)

        print(f"تم تحليل الصورة بنجاح!")
        print(f" - الطول التقديري بالبكسل (Height/Length): {h} px")
        print(f" - العرض التقديري بالبكسل (Width): {w} px")

        return {"height_px": h, "width_px": w, "contours_count": len(contours)}
    else:
        print("لم يتم العثور على حواف واضحة في الصورة.")
        return None

if __name__ == '__main__':
    # تجربة افتراضية لفحص السكربت (سنقوم لاحقاً برفع صورة حقيقية واختبارها)
    print("جاري اختبار معالجة الصور لنظام الطب الشرعي...")
