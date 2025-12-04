from pymongo import MongoClient

# Replace with your actual URI from .env
uri = "mongodb+srv://mtiwary982_db_user:Mohit982@cluster0.04ufp56.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri)
    # Try listing databases
    print("✅ Connected successfully!")
    print("Databases:", client.list_database_names())
except Exception as e:
    print("❌ Connection failed:", e)