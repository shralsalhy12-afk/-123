from database import get_supabase_client

def add_unidentified_remains(location, age, sex, stature, image_path, notes):
    """
    إدخال حالة هيكل عظمي / رفات مجهول جديدة مباشرة إلى جدول unidentified_remains في Supabase
    """
    # الحصول على الاتصال المشفر مع Supabase
    supabase = get_supabase_client()

    # تجهيز البيانات كقاموس (Dictionary) متوافق مع بنية أعمدة جدول PostgreSQL
    data = {
        "recovery_location": location,
        "estimated_age": str(age),
        "estimated_sex": str(sex),
        "stature": float(stature) if stature else 0.0,
        "bone_image_path": str(image_path),
        "analysis_notes": str(notes)
    }

    # تنفيذ أمر الإدخال (Insert)
    response = supabase.table("unidentified_remains").insert(data).execute()
    
    print("تم تسجيل حالة الهيكل العظمي المجهول بنجاح تام في قاعدة بيانات Supabase السحابية!")
    return response

if __name__ == '__main__':
    # تجربة إدخال حالة افتراضية لفحص الاتصال والتخزين
    add_unidentified_remains(
        location="قطاع غزة - المنطقة الجنوبية",
        age="25-35",
        sex="غير محدد (يتطلب فحص عظم الحوض)",
        stature=172.5,
        image_path="samples/bone_sample_01.jpg",
        notes="تم العثور على آثار التئام قديمة في عظم الفخذ الأيمن، وجود صفيحة معدنية جراحية."
    )
