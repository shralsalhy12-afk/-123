import streamlit as st
import sqlite3
from database import init_db
from add_case import add_unidentified_remains
from add_missing_person import add_missing_person

# إعدادات الصفحة
st.set_page_config(page_title="نظام المساعدة في الطب الشرعي - غزة", layout="wide")

# تهيئة قاعدة البيانات عند تشغيل التطبيق
init_db()

st.title("🧬 نظام المساعدة في الطب الشرعي والتعرف على المفقودين")
st.markdown("منظومة رقمية ذكية لمطابقة الرفات المجهولة مع بلاغات العائلات بناءً على القياسات، العلامات الجراحية، والـ DNA.")

# القائمة الجانبية للتنقل بين الأقسام
menu = ["إضافة بلاغ مفقود (عائلة)", "تسجيل رفات مجهول (ميداني)", "قائمة الحالات وسجلات المطابقة"]
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
        bone_image_path = st.text_input("مسار صورة العظم أو الأشعة (مثال: samples/bone.jpg)", value="samples/bone.jpg")
        analysis_notes = st.text_area("ملاحظات الطب الشرعي والماركرز الفارقة (صفائح، علامات مرضية)")

        submit_remains = st.form_submit_button("حفظ حالة الرفات")

        if submit_remains and location:
            add_unidentified_remains(location, estimated_age, estimated_sex, stature, bone_image_path, analysis_notes)
            st.success("تم تسجيل حالة الرفات المجهول بنجاح في قاعدة البيانات!")

# 3. قسم عرض الحالات والمطابقة
elif choice == "قائمة الحالات وسجلات المطابقة":
    st.header("🔍 سجلات النظام ومحرك المطابقة الذكي")

    conn = sqlite3.connect('forensic_system.db')
    cursor = conn.cursor()

    st.subheader("📁 الرفات المجهولة المسجلة:")
    cursor.execute("SELECT remains_id, recovery_location, estimated_age, estimated_sex, stature FROM unidentified_remains")
    remains_list = cursor.fetchall()

    if remains_list:
        for r in remains_list:
            st.write(f"**معرف الرفات:** {r[0]} | **المكان:** {r[1]} | **العمر:** {r[2]} | **الجنس:** {r[3]} | **الطول:** {r[4]} سم")
    else:
        st.info("لا توجد حالات رفات مسجلة حتى الآن.")

    st.markdown("---")
    st.subheader("📋 بلاغات المفقودين المسجلة:")
    cursor.execute("SELECT missing_id, full_name, age_range, gender, has_dna_sample FROM missing_persons")
    missing_list = cursor.fetchall()

    if missing_list:
        for m in missing_list:
            st.write(f"**معرف المفقود:** {m[0]} | **الاسم:** {m[1]} | **العمر:** {m[2]} | **الجنس:** {m[3]} | **DNA متوفر:** {'نعم' if m[4] else 'لا'}")
    else:
        st.info("لا توجد بلاغات مفقودين مسجلة حتى الآن.")

    conn.close()
