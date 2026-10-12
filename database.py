import os
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """
    إنشاء الاتصال الآمن والمشفر مع قاعدة بيانات Supabase
    """
    SUPABASE_URL = "https://jawekdpqyrkagxrojasq.supabase.co"
    SUPABASE_KEY = "sb_publishable_1dlv4ebKYXLynML928VPkw_cUU6nGJI"
    
    url = os.environ.get("SUPABASE_URL", SUPABASE_URL)
    key = os.environ.get("SUPABASE_KEY", SUPABASE_KEY)
    
    return create_client(url, key)

def init_db():
    """
    دالة التحقق من اتصال قاعدة البيانات
    """
    try:
        supabase = get_supabase_client()
        # اختبار اتصال سريع بجدول المفقودين
        supabase.table("missing_persons").select("missing_id").limit(1).execute()
        print("تم الاتصال بقاعدة بيانات Supabase بنجاح تام!")
    except Exception as e:
        print(f"تنبيه الاتصال: {e}")

if __name__ == '__main__':
    init_db()
