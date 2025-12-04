import asyncio, random
from datetime import datetime, timedelta
from app.core.db import db

TYPES = ["harassment","theft","unsafe_area","hazard","emergency"]
BASE = (27.195, 88.503)

async def run():
    docs=[]
    for i in range(50):
        lat = BASE[0] + random.uniform(-0.02, 0.02)
        lng = BASE[1] + random.uniform(-0.02, 0.02)
        t = random.choice(TYPES)
        docs.append({
            "type": t, "severity": random.randint(1,5), "description": f"Seed {t} case {i}",
            "lat": lat, "lng": lng, "f_lat": round(lat,3), "f_lng": round(lng,3),
            "consent_public_map": True, "media_urls": [], "status": "verified",
            "created_at": datetime.utcnow() - timedelta(minutes=random.randint(0, 1000))
        })
    await db.incidents.delete_many({})
    await db.incidents.insert_many(docs)
    print("Seeded 50 incidents.")

if __name__ == "__main__":
    asyncio.run(run())