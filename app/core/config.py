import os

class Settings:
    MONGO_URI = os.getenv("MONGO_URI", "")
    DB_NAME = os.getenv("DB_NAME", "safecity")
    JWT_SECRET = os.getenv("JWT_SECRET", "devsecret")
    CLOUDINARY_CLOUD = os.getenv("CLOUDINARY_CLOUD", "")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

settings = Settings()