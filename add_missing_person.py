import sqlite3

def add_missing_person(full_name, age_range, gender, medical_history, has_dna_sample):
    """
    وظيفة هذا السكربت: استقبال بلاغات العائلات عن المفقودين وتخزينها 
    في جدول المفقودين لتكون مرجعاً للمطابقة.
    """
    conn = sqlite3.connect('forensic_system.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO missing_persons 
        (full_name, age_range, gender, medical_history, has_dna_sample)
        VALUES (?, ?, ?, ?, ?)
    ''', (full_name, age_range, gender, medical_history, has_dna_sample))

    conn.commit()
    conn.close()
    print(f"تم تسجيل بلاغ المفقود ({full_name}) بنجاح في قاعدة البيانات!")

if __name__ == '__main__':
    # تجربة إدخال بلاغ مفقود افتراضي يحتوي على علامات طبية فارقة (مثل الصفيحة الجراحية)
    add_missing_person(
        full_name="محمد أحمد العبدالله",
        age_range="25-35",
        gender="ذكر",
        medical_history="وجود صفيحة معدنية جراحية في عظم الفخذ الأيمن، لا توجد أمراض مزمنة.",
        has_dna_sample=True
    )
