import streamlit as st
import os
from database import get_supabase_client, init_db
from add_case import add_unidentified_remains
from add_missing_person import add_missing_person
from matching_engine import calculate_match_score

# إعدادات الصفحة
st.set_page_config(page_title="نظام المساعدة في الطب الشرعي - غزة", layout="wide")

# تهيئة واختبار الاتصال بقاعدة البيانات عند تشغيل التطبيق
init_db()

# الحصول على عميل Supabase المشفر
supabase = get_supabase_client()

st.title("🧬 نظام المساعدة في الطب الشرعي والتعرف على المفقودين")
st.markdown("منظومة رقمية ذكية لمطابقة الرفات المجهولة مع بلاغات العائلات بناءً على القياسات، العلامات الجراحية، والـ DNA.")

# القائمة الجانبية للتنقل بين الأقسام
menu = ["إضافة بلاغ مفقود (عائلة)", "تسجيل رفات مجهول (ميداني)", "سجلات النظام ومحرك المطابقة الذكي"]
choice = st.sidebar.selectbox("اختر القسم:", menu)

# 1. قسم إضافة بلاغ مفقود
if choice == "إضافة بلاغ مفقود (عائلة)":
    st.header("📋 تسجيل بلاغ جديد عن مفقود")
    
    with st.form("missing_form"):
        full_name = st.text_input("الاسم الكامل للمفقود")
        col1, col2 = st.columns(2)
        with col1:
            age_range = st.text_input("النطاق العمري (مثال: 25-35)")
        with col2:
            gender = st.selectbox("الجنس", ["ذكر", "أنثى", "غير محدد"])
            
        medical_history = st.text_area("السجل الطبي والعلامات الفارقة (مثل: عمليات جراحية، صفائح معدنية، كسور سابقة)")
        has_dna = st.checkbox("هل توجد عينة DNA متوفرة للفحص؟")
        
        submit_missing = st.form_submit_button("حفظ بلاغ المفقود")
        
        if submit_missing and full_name:
            try:
                add_missing_person(full_name, age_range, gender, medical_history, has_dna)
                st.success(f"تم تسجيل بلاغ المفقود ({full_name}) بنجاح في قاعدة البيانات السحابية!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء حفظ البلاغ: {e}")

# 2. قسم تسجيل رفات مجهول (نموذج متكامل مع رفع الصور بضغطة واحدة)
elif choice == "تسجيل رفات مجهول (ميداني)":
    st.header("🦴 تسجيل حالة هيكل عظمي / رفات مجهول جديد")
    st.markdown("أدخل بيانات الرفات وارفع الصور المرفقة، ثم اضغط زر الحفظ النهائي في الأسفل.")

    with st.form("unified_remains_form"):
        location = st.text_input("مكان الاستخراج / العثور")
        col1, col2 = st.columns(2)
        with col1:
            estimated_age = st.text_input("العمر التقديري")
        with col2:
            estimated_sex = st.text_input("الجنس التقديري")
            
        stature = st.number_input("الطول التقديري (بالسنتيمتر)", min_value=0.0, value=170.0)
        analysis_notes = st.text_area("ملاحظات الطب الشرعي والماركرز الفارقة (صفائح، علامات مرضية)")
        
        # حقل رفع الصور
        uploaded_files = st.file_uploader(
            "📷 اختر صور العظام أو الأشعة (يمكنك اختيار أكثر من صورة)", 
            type=["jpg", "jpeg", "png", "dcm"], 
            accept_multiple_files=True
        )
        
        submit_all = st.form_submit_button("💾 حفظ الحالة والملفات بالكامل في النظام")
        
        if submit_all:
            if not location:
                st.error("الرجاء إدخال مكان الاستخراج على الأقل.")
            else:
                try:
                    # معالجة وحفظ الصور المرفوعة إن وجدت
                    saved_paths = []
                    if uploaded_files:
                        os.makedirs("samples", exist_ok=True)
                        for uploaded_file in uploaded_files:
                            file_path = os.path.join("samples", uploaded_file.name)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            saved_paths.append(file_path)
                    
                    bone_image_path_str = ",".join(saved_paths) if saved_paths else "samples/default.jpg"
                    
                    # استدعاء دالة الإضافة السحابية بـ Supabase
                    add_unidentified_remains(
                        location=location,
                        age=estimated_age,
                        sex=estimated_sex,
                        stature=stature,
                        image_path=bone_image_path_str,
                        notes=analysis_notes
                    )
                    st.success("🎉 تم حفظ حالة الرفات مع الصور المرفقة بنجاح تام في قاعدة البيانات السحابية Supabase!")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء حفظ بيانات الرفات: {e}")

# 3. قسم السجلات ومحرك المطابقة التفاعلي
elif choice == "سجلات النظام ومحرك المطابقة الذكي":
    st.header("🔍 محرك المطابقة الذكي وسجلات الحالات السحابية")
    
    try:
        # جلب البيانات مباشرة من جداول Supabase
        remains_res = supabase.table("unidentified_remains").select("*").execute()
        remains_list = remains_res.data if remains_res.data else []
        
        missing_res = supabase.table("missing_persons").select("*").execute()
        missing_list = missing_res.data if missing_res.data else []
    except Exception as e:
        st.error(f"تعذر جلب البيانات من قاعدة البيانات السحابية: {e}")
        remains_list, missing_list = [], []
    
    col_r, col_m = st.columns(2)
    with col_r:
        st.subheader("📁 الرفات المجهولة المسجلة:")
        if remains_list:
            for r in remains_list:
                st.info(f"**معرف الرفات:** {r.get('remains_id')} | **المكان:** {r.get('recovery_location')} | **الطول:** {r.get('stature')} سم\n\n**المسار/الصور:** {r.get('bone_image_path')}\n\n**ملاحظات:** {r.get('analysis_notes')}")
        else:
            st.warning("لا توجد رفات مسجلة حالياً.")
            
    with col_m:
        st.subheader("📋 بلاغات المفقودين المسجلة:")
        if missing_list:
            for m in missing_list:
                st.success(f"**معرف المفقود:** {m.get('missing_id')} | **الاسم:** {m.get('full_name')} | **العمر:** {m.get('age_range')}\n\n**السجل الطبي:** {m.get('medical_history')}")
        else:
            st.warning("لا توجد بلاغات مفقودين مسجلة حالياً.")
            
    st.markdown("---")
    st.subheader("⚡ تشغيل محرك المطابقة والبحث الآلي")
    
    if remains_list and missing_list:
        remains_ids = [r.get('remains_id') for r in remains_list]
        selected_remains_id = st.selectbox("اختر معرف الرفات المجهول المراد فحصه ومطابقته:", remains_ids)
        
        if st.button("🚀 بدء عملية المطابقة والبحث الشامل"):
            selected_remains = next(r for r in remains_list if r.get('remains_id') == selected_remains_id)
            remains_data = {
                "stature": selected_remains.get('stature', 0.0),
                "notes": selected_remains.get('analysis_notes', ""),
                "has_dna": True
            }
            
            st.markdown(f"### نتائج المطابقة للرفات رقم ({selected_remains_id}):")
            
            results = []
            for person in missing_list:
                match_res = calculate_match_score(remains_data, person)
                results.append({
                    "name": person.get('full_name'),
                    "score": match_res["match_percentage"],
                    "reasons": match_res["match_reasons"]
                })
            
            results = sorted(results, key=lambda x: x["score"], reverse=True)
            
            for res in results:
                st.write(f"**المرشح:** {res['name']}")
                st.progress(res['score'] / 100)
                st.write(f"**نسبة التطابق المقترحة:** {res['score']}%")
                if res['reasons']:
                    st.write("**أسباب التشابه ومؤشرات المطابقة:**")
                    for reason in res['reasons']:
                        st.markdown(f"- {reason}")
                st.markdown("---")
    else:
        st.info("الرجاء إدخال حالة رفات واحدة على الأقل وبلاغ مفقود واحد لتفعيل محرك المطابقة.")
