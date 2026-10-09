import sqlite3

def add_unidentified_remains(location, age, sex, stature, image_path, notes):
    # الاتصال بقاعدة البيانات التي أنشأناها مسبقاً
    conn = sqlite3.connect('forensic_system.db')
    cursor = conn.cursor()

    # إدخال بيانات الهيكل العظمي الجديد إلى الجدول
    cursor.execute('''
        INSERT INTO unidentified_remains 
        (recovery_location, estimated_age, estimated_sex, stature, bone_image_path, analysis_notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (location, age, sex, stature, image_path, notes))

    conn.commit()
    conn.close()
    print("تم تسجيل حالة الهيكل العظمي المجهول بنجاح في النظام العالمي!")

if __name__ == '__main__':
    # تجربة إدخال حالة افتراضية لفحص النظام
    add_unidentified_remains(
        location="قطاع غزة - المنطقة الجنوبية",
        age="25-35",
        sex="غير محدد (يتطلب فحص عظم الحوض)",
        stature=172.5,
        image_path="samples/bone_sample_01.jpg",
        notes="تم العثور على آثار التئام قديمة في عظم الفخذ الأيمن، وجود صفيحة معدنية جراحية."
    )
