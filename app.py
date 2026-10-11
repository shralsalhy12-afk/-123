import streamlit as st
import sqlite3
from database import init_db
from add_case import add_unidentified_remains
from add_missing_person import add_missing_person
from matching_engine import calculate_match_score

# إعدادات الصفحة
st.set_page_config(page_title="نظام المساعدة في الطب الشرعي - غزة", layout="wide")

# تهيئة قاعدة البيانات عند تشغيل التطبيق
init_db()

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
            add_missing_person(full_name, age_range, gender, medical_history, has_dna)
            st.success(f"تم تسجيل بلاغ المفقود ({full_name}) بنجاح!")

# 2. قسم تسجيل رفات مجهول
elif choice == "تسجيل رفات مجهول (ميداني)":
    st.header("🦴 تسجيل حالة هيكل عظمي / رفات مجهول")
    
    with st.form("remains_form"):
        location = st.text_input("مكان الاستخراج / العثور")
        col1, col2 = st.columns(2)
        with col1:
            estimated_age = st.text_input("العمر التقديري")
        with col2:
            estimated_sex = st.text_input("الجنس التقديري")
            
        stature = st.number_input("الطول التقديري (بالسنتيمتر)", min_value=0.0, value=170.0)
        bone_image_path = st.text_input("مسار صورة العظم أو الأشعة", value="samples/bone.jpg")
        analysis_notes = st.text_area("ملاحظات الطب الشرعي والماركرز الفارقة (صفائح، علامات مرضية)")
        
        submit_remains = st.form_submit_button("حفظ حالة الرفات")
        
        if submit_remains and location:
            add_unidentified_remains(location, estimated_age, estimated_sex, stature, bone_image_path, analysis_notes)
            st.success("تم تسجيل حالة الرفات المجهول بنجاح في قاعدة البيانات!")

# 3. قسم السجلات ومحرك المطابقة التفاعلي
elif choice == "سجلات النظام ومحرك المطابقة الذكي":
    st.header("🔍 محرك المطابقة الذكي وسجلات الحالات")
    
    conn = sqlite3.connect('forensic_system.db')
    cursor = conn.cursor()
    
    # جلب الرفات المسجلة
    cursor.execute("SELECT remains_id, recovery_location, estimated_age, estimated_sex, stature, analysis_notes FROM unidentified_remains")
    remains_list = cursor.fetchall()
    
    # جلب بلاغات المفقودين المسجلة
    cursor.execute("SELECT missing_id, full_name, age_range, gender, medical_history, has_dna_sample FROM missing_persons")
    missing_list = cursor.fetchall()
    
    col_r, col_m = st.columns(2)
    with col_r:
        st.subheader("📁 الرفات المجهولة المسجلة:")
        if remains_list:
            for r in remains_list:
                st.info(f"**معرف الرفات:** {r[0]} | **المكان:** {r[1]} | **الطول:** {r[4]} سم\n\n**ملاحظات:** {r[5]}")
        else:
            st.warning("لا توجد رفات مسجلة.")
            
    with col_m:
        st.subheader("📋 بلاغات المفقودين المسجلة:")
        if missing_list:
            for m in missing_list:
                st.success(f"**معرف المفقود:** {m[0]} | **الاسم:** {m[1]} | **العمر:** {m[2]}\n\n**السجل الطبي:** {m[4]}")
        else:
            st.warning("لا توجد بلاغات مفقودين مسجلة.")
            
    st.markdown("---")
    st.subheader("⚡ تشغيل محرك المطابقة والبحث الآلي")
    
    if remains_list and missing_list:
        selected_remains_id = st.selectbox("اختر معرف الرفات المجهول المراد فحصه ومطابقته:", [r[0] for r in remains_list])
        
        if st.button("🚀 بدء عملية المطابقة والبحث الشامل"):
            # استخراج بيانات الرفات المختار
            selected_remains = next(r for r in remains_list if r[0] == selected_remains_id)
            remains_data = {
                "stature": selected_remains[4],
                "notes": selected_remains[5],
                "has_dna": True # افتراضي للتحليل
            }
            
            st.markdown(f"### نتائج المطابقة للرفات رقم ({selected_remains_id}):")
            
            results = []
            for person in missing_list:
                match_res = calculate_match_score(remains_data, person)
                results.append({
                    "name": person[1],
                    "score": match_res["match_percentage"],
                    "reasons": match_res["match_reasons"]
                })
            
            # ترتيب النتائج تنازلياً حسب نسبة التطابق
            results = sorted(results, key=lambda x: x["score"], reverse=True)
            
            for res in results:
                # عرض النسبة بلون أو متر تفاعلي
                st.write(🇪🇬 f"**المرشح:** {res['name']}")
                st.progress(res['score'] / 100)
                st.write(f"**نسبة التطابق المقترحة:** {res['score']}%")
                if res['reasons']:
                    st.write("**أسباب التشابه ومؤشرات المطابقة:**")
                    for reason in res['reasons']:
                        st.markdown(f"- {reason}")
                st.markdown("---")
    else:
        st.info("الرجاء إدخال حالة رفات واحدة على الأقل وبلاغ مفقود واحد لتفعيل محرك المطابقة.")
        
    conn.close()
