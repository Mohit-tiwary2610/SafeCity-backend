from pymongo import MongoClient

uri = "mongodb+srv://mtiwary982_db_user:Mohit982@cluster0.04ufp56.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

db = client["safecity"]
incidents = db["incidents"]

sample_data = [
    {
        "title": "Streetlight not working",
        "description": "Dark street near Golmuri market",
        "location": "Golmuri, Jamshedpur",
        "severity": "medium"
    },
    {
        "title": "Road accident",
        "description": "Minor collision at Jugsalai crossing",
        "location": "Jugsalai, Jamshedpur",
        "severity": "high"
    },
    {
        "title": "Garbage pile",
        "description": "Uncollected waste near Sakchi bazaar",
        "location": "Sakchi, Jamshedpur",
        "severity": "low"
    }
]

result = incidents.insert_many(sample_data)
print("✅ Seeded incidents with IDs:", result.inserted_ids)