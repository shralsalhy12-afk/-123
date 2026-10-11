import sqlite3
from database import init_db
from add_case import add_unidentified_remains
from add_missing_person import add_missing_person
from matching_engine import search_and_match
from image_processor import analyze_bone_image
import os

def run_system_test():
    print("==========================================")
    print(" بدء الاختبار الشامل لنظام المساعدة في الطب الشرعي")
    print("==========================================")

    # 1. تهيئة قاعدة البيانات
    print("\n[1] جاري إنشاء وتهيئة قاعدة البيانات...")
    init_db()

    # 2. إضافة بلاغ مفقود تجريبي
    print("\n[2] جاري تسجيل بلاغ مفقود جديد...")
    add_missing_person(
        full_name="سامر أحمد الجعبري",
        age_range="28-35",
        gender="ذكر",
        medical_history="وجود صفيحة معدنية جراحية في عظم الفخذ الأيمن نتيجة إصابة سابقة.",
        has_dna_sample=True
    )

    # 3. إدخال حالة رفات مجهول جديد
    print("\n[3] جاري تسجيل هيكل عظمي مجهول تم العثور عليه...")
    add_unidentified_remains(
        location="قطاع غزة - المحافظة الوسطى",
        age="30",
        sex="ذكر",
        stature=174.0,
        image_path="samples/test_bone.jpg",
        notes="تم العثور على صفيحة معدنية جراحية مطابقة في عظم الفخذ الأيمن، وسلامة الهيكل العام."
    )

    # 4. محاكاة تحليل صورة عظم افتراضية (إن وجدت)
    print("\n[4] جاري فحص وحدة معالجة الصور...")
    os.makedirs("samples", exist_ok=True)
    dummy_image_path = "samples/test_bone.jpg"

    # إنشاء صورة تجريبية فارغة للتأكد من عمل السكربت دون أخطاء
    import numpy as np
    import cv2
    dummy_img = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.rectangle(dummy_img, (50, 50), (150, 250), (255, 255, 255), -1)
    cv2.imwrite(dummy_image_path, dummy_img)

    analyze_bone_image(dummy_image_path)

    # 5. تشغيل محرك المطابقة للبحث عن التطابقات
    print("\n[5] جاري تشغيل محرك المطابقة متعدد الطبقات...")
    # الهيكل الذي أضفناه سيكون برقم ID يساوي 1 غالباً
    search_and_match(remains_id=1)

    print("\n==========================================")
    print(" تم الانتهاء من الاختبار الشامل بنجاح باهر!")
    print("==========================================")

if __name__ == '__main__':
    run_system_test()
