from database import get_supabase_client

def add_missing_person(full_name, age_range, gender, medical_history, has_dna_sample):
    """
    وظيفة هذا السكربت: استقبال بلاغات العائلات عن المفقودين وتخزينها 
    في جدول المفقودين بـ Supabase لتكون مرجعاً للمطابقة.
    """
    # الحصول على الاتصال المشفر مع Supabase
    supabase = get_supabase_client()

    # تجهيز البيانات كقاموس (Dictionary) متوافق مع بنية أعمدة جدول PostgreSQL
    data = {
        "full_name": str(full_name),
        "age_range": str(age_range),
        "gender": str(gender),
        "medical_history": str(medical_history),
        "has_dna_sample": bool(has_dna_sample)
    }

    # تنفيذ أمر الإدخال (Insert) في جدول missing_persons
    response = supabase.table("missing_persons").insert(data).execute()
    
    print(f"تم تسجيل بلاغ المفقود ({full_name}) بنجاح تام في قاعدة بيانات Supabase!")
    return response

if __name__ == '__main__':
    # تجربة إدخال بلاغ مفقود افتراضي يحتوي على علامات طبية فارقة (مثل الصفيحة الجراحية)
    add_missing_person(
        full_name="محمد أحمد العبدالله",
        age_range="25-35",
        gender="ذكر",
        medical_history="وجود صفيحة معدنية جراحية في عظم الفخذ الأيمن، لا توجد أمراض مزمنة.",
        has_dna_sample=True
    )
