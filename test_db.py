from db_client import check_db_connection

if __name__ == "__main__":
    result = check_db_connection()
    if result:
        print("✅ تم الاتصال بقاعدة البيانات بنجاح!")
    else:
        print("❌ فشل الاتصال، تأكد من مفتاح SUPABASE_SERVICE_ROLE_KEY في ملف .env")