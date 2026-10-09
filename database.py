import sqlite3

def init_db():
    conn = sqlite3.connect('forensic_system.db')
    cursor = conn.cursor()

    # جدول المفقودين (بلاغات العائلات)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS missing_persons (
            missing_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            age_range TEXT,
            gender TEXT,
            medical_history TEXT,
            has_dna_sample BOOLEAN
        )
    ''')

    # جدول الرفات والهياكل المجهولة (مع مسار صورة العظم والقياسات)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unidentified_remains (
            remains_id INTEGER PRIMARY KEY AUTOINCREMENT,
            recovery_location TEXT,
            estimated_age TEXT,
            estimated_sex TEXT,
            stature REAL,
            bone_image_path TEXT,
            analysis_notes TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Database created successfully!")

if __name__ == '__main__':
    init_db()
