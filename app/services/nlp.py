import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

CLASSES = ["harassment", "theft", "unsafe_area", "hazard", "emergency"]
model: Pipeline | None = None

def clean(t: str) -> str:
    return re.sub(r"\s+", " ", t.lower()).strip()

def train(texts, labels):
    global model
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1)),
        ("clf", LogisticRegression(max_iter=400))
    ])
    model.fit([clean(x) for x in texts], labels)

def predict(text: str) -> str:
    t = clean(text)
    if not model:
        if any(k in t for k in ["stole", "theft", "rob", "pickpocket"]): return "theft"
        if any(k in t for k in ["harass", "stalk", "catcall"]): return "harassment"
        if any(k in t for k in ["dark", "unsafe", "creepy"]): return "unsafe_area"
        if any(k in t for k in ["pothole", "broken", "leak", "wire"]): return "hazard"
        return "emergency" if any(k in t for k in ["attack", "knife", "urgent"]) else "unsafe_area"
    return CLASSES[model.predict([t])[0]]