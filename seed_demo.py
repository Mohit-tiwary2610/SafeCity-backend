import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Use the same Atlas URI you already configured in your .env
MONGO_URI = "mongodb+srv://mtiwary982_db_user:Mohit982@cluster0.04ufp56.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGO_URI)
db = client["safecity"]   # ✅ lowercase to avoid case conflict

demo_incidents = [
    {"type": "hazard", "severity": "high", "description": "Pipe burst near Golmuri park", "lat": 22.802, "lng": 86.202},
    {"type": "unsafe_area", "severity": "medium", "description": "Streetlight not working near Golmuri market", "lat": 22.804, "lng": 86.205},
    {"type": "emergency", "severity": "high", "description": "Minor collision at Jugsalai crossing", "lat": 22.798, "lng": 86.195},
    {"type": "theft", "severity": "low", "description": "Pickpocketing reported at Sakchi bazaar", "lat": 22.805, "lng": 86.210},
    {"type": "harassment", "severity": "medium", "description": "Verbal harassment near Bistupur bus stand", "lat": 22.790, "lng": 86.180},
    {"type": "hazard", "severity": "low", "description": "Open manhole near Kadma market", "lat": 22.815, "lng": 86.220},
    {"type": "unsafe_area", "severity": "high", "description": "Dark alley near Sonari riverbank", "lat": 22.782, "lng": 86.175},
    {"type": "emergency", "severity": "medium", "description": "Small fire at Telco colony", "lat": 22.820, "lng": 86.230},
    {"type": "theft", "severity": "high", "description": "Bike theft near Adityapur railway station", "lat": 22.785, "lng": 86.170},
    {"type": "harassment", "severity": "low", "description": "Catcalling reported near Mango bridge", "lat": 22.812, "lng": 86.240},
    {"type": "hazard", "severity": "medium", "description": "Broken traffic signal at Sakchi roundabout", "lat": 22.807, "lng": 86.215},
    {"type": "unsafe_area", "severity": "low", "description": "Poor lighting near Baridih colony", "lat": 22.825, "lng": 86.250},
    {"type": "emergency", "severity": "high", "description": "Gas leak reported near Burmamines", "lat": 22.795, "lng": 86.185},
    {"type": "theft", "severity": "medium", "description": "Mobile snatching near Dimna road", "lat": 22.830, "lng": 86.260},
    {"type": "harassment", "severity": "high", "description": "Physical harassment case near Jubilee Park", "lat": 22.800, "lng": 86.190},
]

async def seed():
    for inc in demo_incidents:
        inc.update({
            "consent_public_map": True,
            "media_urls": [],
            "status": "pending",
            "created_at": datetime.utcnow(),
        })
        await db.incidents.insert_one(inc)
    print("✅ 15 demo incidents inserted into MongoDB Atlas!")

asyncio.run(seed())