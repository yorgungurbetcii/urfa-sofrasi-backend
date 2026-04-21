Python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
from datetime import datetime

app = FastAPI()

# Firebase init (ENV üzerinden)
firebase_json = os.environ.get("FIREBASE_KEY")

cred = credentials.Certificate(json.loads(firebase_json))
firebase_admin.initialize_app(cred)

db = firestore.client()

# MODELS
class Item(BaseModel):
    name: str
    price: float
    quantity: int

class Order(BaseModel):
    table: str
    items: List[Item]

@app.get("/")
def root():
    return {"status": "OK - Urfa Sofrasi API 🔥"}

@app.get("/menu")
def get_menu():
    docs = db.collection("menus").stream()
    return [doc.to_dict() for doc in docs]

@app.post("/order")
def create_order(order: Order):

    total = sum(i.price * i.quantity for i in order.items)

    data = {
        "table": order.table,
        "items": [i.dict() for i in order.items],
        "total": total,
        "status": "new",
        "created_at": datetime.utcnow()
    }

    db.collection("orders").add(data)

    return {"message": "Siparis alindi ✅", "total": total}
