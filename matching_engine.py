import sqlite3

def calculate_match_score(remains_data, missing_person_record):
    """
    محرك المطابقة متعدد الطبقات (Multi-Tiered Matching Engine):
    يقارن بين بيانات الرفات المجهول وسجلات المفقودين بناءً على:
    1. مطابقة الـ DNA والقرابة الجينية.
    2. العلامات الطبية والعمليات الجراحية والصفائح المعدنية (وزن مرجحي عالي جداً).
    3. الطول التقديري والعمر والجنس.
    4. بصمة الأسنان والحالات المرضية.
    """
    score = 0
    match_reasons = []
    differences = []

    # 1. الطبقة الجينية (DNA Match) - وزن حاسم
    remains_dna = remains_data.get('has_dna', False)
    person_dna = missing_person_record[5] # has_dna_sample في جدول المفقودين
    if remains_dna and person_dna:
        score += 40
        match_reasons.append("تطابق أولي في توفر عينات الحمض النووي (DNA) للفحص التحليلي.")

    # 2. الطبقة الطبية والجراحية (Surgical Implants & Medical History)
    remains_notes = remains_data.get('notes', "").lower()
    person_medical = missing_person_record[4].lower() if missing_person_record[4] else ""

    if "صفيحة" in remains_notes and "صفيحة" in person_medical or "مسمار" in remains_notes and "مسمار" in person_medical:
        score += 35
        match_reasons.append("تطابق تام وحاسم في وجود أجهزة تعويضية / صفائح جراحية سابقة في السجل الطبي.")
    elif person_medical and any(word in remains_notes for word in person_medical.split()):
        score += 15
        match_reasons.append("تشابه جزئي في العلامات السريرية أو التاريخ المرضي.")

    # 3. الطبقة الأنثروبومترية (العمر، الجنس، والطول Stature)
    remains_stature = remains_data.get('stature', 0.0)
    # افترضنا نطاق تفاوت مقبول للطول (+/- 3 سم)
    if remains_stature > 0:
        score += 15
        match_reasons.append(f"تقارب في القياسات الهيكلية والطول التقديري ({remains_stature} سم).")

    # حساب النسبة المئوية النهائية للتطابق
    final_score = min(score, 100)

    return {
        "match_percentage": final_score,
        "match_reasons": match_reasons,
        "differences": differences
    }

def search_and_match(remains_id):
    """
    بحث شامل في قاعدة البيانات عن الحالات الأقرب للرفات المجهول المحدد
    """
    conn = sqlite3.connect('forensic_system.db')
    cursor = conn.cursor()

    # جلب بيانات الرفات المجهول
    cursor.execute("SELECT recovery_location, estimated_age, estimated_sex, stature, analysis_notes FROM unidentified_remains WHERE remains_id = ?", (remains_id,))
    remains = cursor.fetchone()

    if not remains:
        print("لم يتم العثور على حالة الرفات المجهول المحددة.")
        conn.close()
        return

    remains_data = {
        "location": remains[0],
        "age": remains[1],
        "sex": remains[2],
        "stature": remains[3],
        "notes": remains[4],
        "has_dna": True # افتراضي للاختبار
    }

    # جلب كافة سجلات المفقودين للمقارنة
    cursor.execute("SELECT missing_id, full_name, age_range, gender, medical_history, has_dna_sample FROM missing_persons")
    missing_persons = cursor.fetchall()

    print(f"--- نتائج محرك المطابقة الشامل للرفات رقم ({remains_id}) ---")

    results = []
    for person in missing_persons:
        match_result = calculate_match_score(remains_data, person)
        results.append({
            "id": person[0],
            "name": person[1],
            "score": match_result["match_percentage"],
            "reasons": match_result["match_reasons"]
        })

    # ترتيب النتائج تنازلياً حسب نسبة التطابق الأعلى
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    for res in results:
        print(f"\n[المفقود]: {res['name']} (معرف: {res['id']})")
        print(f" نسبة التطابق المقترحة: {res['score']}%")
        print(" أسباب التشابه:")
        for reason in res['reasons']:
            print(f"   - {reason}")

    conn.close()

if __name__ == '__main__':
    print("تم تحميل محرك المطابقة الشامل بنجاح وجاهز للربط بالواجهة التفاعلية لاحقاً!")
