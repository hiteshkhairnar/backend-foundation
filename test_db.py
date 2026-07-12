from app.database.database import engine

try:
    connection = engine.connect()
    print("=" * 40)
    print("✅ Database Connected Successfully!")
    print("=" * 40)
    connection.close()
except Exception as e:
    print("=" * 40)
    print("❌ Database Connection Failed")
    print("=" * 40)
    print(e)