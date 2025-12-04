from fastapi import APIRouter
from app.core.db import db

router = APIRouter()

@router.get("/fairness")
async def fairness():
    try:
        pipeline = [
            {
                "$match": {
                    "status": {"$in": ["pending", "verified"]},
                    "f_lat": {"$ne": None},
                    "f_lng": {"$ne": None},
                }
            },
            {
                "$group": {
                    "_id": {
                        "type": "$type",
                        "f_lat": "$f_lat",
                        "f_lng": "$f_lng",
                        "severity": "$severity",
                    },
                    "count": {"$sum": 1},
                }
            },
        ]

        agg = [a async for a in db.incidents.aggregate(pipeline)]
        dist = [
            {
                "type": a["_id"].get("type"),
                "f_lat": a["_id"].get("f_lat"),
                "f_lng": a["_id"].get("f_lng"),
                "severity": a["_id"].get("severity"),
                "count": a["count"],
            }
            for a in agg
        ]

        return {
            "distribution": dist,
            "moderationLag": 0,
            "falsePositiveRate": 0.05,
        }
    except Exception as e:
        return {
            "error": str(e),
            "distribution": [],
            "moderationLag": None,
            "falsePositiveRate": None,
        }


@router.get("/heatmap")
async def heatmap():
    try:
        pipeline = [
            {
                "$match": {
                    "status": {"$in": ["pending", "verified"]},
                    "f_lat": {"$ne": None},
                    "f_lng": {"$ne": None},
                }
            },
            {
                "$project": {
                    "type": 1,
                    "f_lat": 1,
                    "f_lng": 1,
                    "severity": 1,
                }
            },
        ]

        points = [p async for p in db.incidents.aggregate(pipeline)]
        heatmap_data = [
            {
                "lat": p.get("f_lat"),
                "lng": p.get("f_lng"),
                "severity": p.get("severity", 1),
            }
            for p in points
        ]

        return {"heatmap": heatmap_data}
    except Exception as e:
        return {"error": str(e), "heatmap": []}