from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = FastAPI()

# Firebase bağlantısı
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# MODELLER
class OrderItem(BaseModel):
    name: str
    price: float
    quantity: int

class Order(BaseModel):
    table: str
    items: List[OrderItem]
    total: float

# TEST
@app.get("/")
def root():
    return {"message": "Urfa Sofrasi API Calisiyor 🔥"}

# Sipariş gönderme
@app.post("/order")
def create_order(order: Order):
    db.collection("orders").add(order.dict())
    return {"status": "Siparis alindi ✅"}
