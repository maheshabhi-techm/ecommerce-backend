from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import (
    auth,
    profile,
    category,
    seller_product,
    customer_product,
    cart,
    order,
    payment,
)
from .database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "The E-commerce application development started"}


app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(category.router)
app.include_router(seller_product.router)
app.include_router(customer_product.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(payment.router)
