import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "safecity")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set. Check your .env file.")

# Use TLS explicitly
client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=False  # safer, don’t bypass certs
)

db = client[DB_NAME]