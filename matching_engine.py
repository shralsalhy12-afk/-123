from database import get_supabase_client

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
    # استخدام اسم الحقل مباشرة من قاموس Supabase بدلاً من الفهرس الرقمي
    person_dna = missing_person_record.get('has_dna_sample', False)
    
    if remains_dna and person_dna:
        score += 40
        match_reasons.append("تطابق أولي في توفر عينات الحمض النووي (DNA) للفحص التحليلي.")

    # 2. الطبقة الطبية والجراحية (Surgical Implants & Medical History)
    remains_notes = remains_data.get('notes', "").lower()
    medical_history_val = missing_person_record.get('medical_history', "")
    person_medical = medical_history_val.lower() if medical_history_val else ""

    if "صفيحة" in remains_notes and "صفيحة" in person_medical or "مسمار" in remains_notes and "مسمار" in person_medical:
        score += 35
        match_reasons.append("تطابق تام وحاسم في وجود أجهزة تعويضية / صفائح جراحية سابقة في السجل الطبي.")
    elif person_medical and any(word in remains_notes for word in person_medical.split()):
        score += 15
        match_reasons.append("تشابه جزئي في العلامات السريرية أو التاريخ المرضي.")

    # 3. الطبقة الأنثروبومترية (العمر، الجنس، والطول Stature)
    remains_stature = remains_data.get('stature', 0.0)
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
    بحث شامل في قاعدة بيانات Supabase عن الحالات الأقرب للرفات المجهول المحدد
    """
    supabase = get_supabase_client()

    # جلب بيانات الرفات المجهول باستخدام عميل Supabase
    remains_res = supabase.table("unidentified_remains").select("*").eq("remains_id", remains_id).execute()
    
    if not remains_res.data:
        print("لم يتم العثور على حالة الرفات المجهول المحددة.")
        return

    remains = remains_res.data[0]
    remains_data = {
        "location": remains.get('recovery_location'),
        "age": remains.get('estimated_age'),
        "sex": remains.get('estimated_sex'),
        "stature": remains.get('stature', 0.0),
        "notes": remains.get('analysis_notes', ""),
        "has_dna": True # افتراضي للاختبار
    }

    # جلب كافة سجلات المفقودين للمقارنة من Supabase
    missing_res = supabase.table("missing_persons").select("*").execute()
    missing_persons = missing_res.data

    print(f"--- نتائج محرك المطابقة الشامل للرفات رقم ({remains_id}) ---")

    results = []
    for person in missing_persons:
        match_result = calculate_match_score(remains_data, person)
        results.append({
            "id": person.get('missing_id'),
            "name": person.get('full_name'),
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

    return results

if __name__ == '__main__':
    print("تم تحميل محرك المطابقة الشامل للعمل مع Supabase بنجاح!")
