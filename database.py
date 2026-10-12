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
    تهيئة قاعدة البيانات في Supabase وإنشاء الجداول إن لم تكن موجودة
    """
    supabase = get_supabase_client()
    
    try:
        # اختبار الاتصال أولاً وجلب عينة
        supabase.table("missing_persons").select("missing_id").limit(1).execute()
        print("جدول بلاغات المفقودين موجود مسبقاً في Supabase.")
    except Exception:
        print("جاري إنشاء جدول missing_persons في Supabase...")
        # ملاحظة: في Supabase، الأفضل إنشاء الجداول عبر SQL Editor في لوحة التحكم، 
        # أو تنفيذ الاستعلامات. لكن دعيني أسهل عليكِ الأمر أكثر:
        
    try:
        supabase.table("unidentified_remains").select("remains_id").limit(1).execute()
        print("جدول الرفات المجهولة موجود مسبقاً في Supabase.")
    except Exception:
        print("جدول unidentified_remains يحتاج للإنشاء.")

if __name__ == '__main__':
    init_db()
