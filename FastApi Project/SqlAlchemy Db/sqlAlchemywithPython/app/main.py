
from fastapi import FastAPI, Depends
from . import Db_model
from .database import engine,  get_db
from .database import SessionLocal
from sqlalchemy.orm import Session
from . import model

app = FastAPI()
Db_model.Base.metadata.create_all(bind=engine)

products = [
    {"id": 1, "name": "Wireless Mouse", "description": "2.4GHz wireless optical mouse", "price": 599.99, "quantity": 50},
    {"id": 2, "name": "Mechanical Keyboard", "description": "Backlit mechanical keyboard with blue switches", "price": 2499.00, "quantity": 30},
    {"id": 3, "name": "USB-C Charger", "description": "65W fast charging USB-C power adapter", "price": 1799.50, "quantity": 100},
    {"id": 4, "name": "Noise Cancelling Headphones", "description": "Over-ear active noise cancelling headphones", "price": 4999.99, "quantity": 20},
    {"id": 5, "name": "Laptop Stand", "description": "Adjustable aluminum laptop stand", "price": 1299.00, "quantity": 75}
]

def init_db ():
    db = SessionLocal()     #This is happening mannually only but we don't want this so will use the dependency injection

    count = db.query(Db_model.Product).count

    if count ==0:

        for product in products:
            db.add(Db_model.Product(**product))

        db.commit() 

init_db()




@app.get("/products")
def get_Product(db :Session = Depends(get_db)):

    db_product = db.query(Db_model.Product).all()

    return {"Message ": "Done",
            "Data":db_product}

@app.get("/products/{id}")
def get_productbyid(id:int ,db :Session = Depends(get_db)):

    db_product = db.query(Db_model.Product).filter(Db_model.Product.id == id).first()

    if db_product:
        return db_product
    return "Product is not Found"

@app.post("/product")
def create_Product(product: model.Product, db :Session = Depends(get_db)):
    db.add(Db_model.Product(**product.model_dump()))
    db.commit()

    return product

@app.put("/product/{id}")
def update_Product(id:int, product:model.Product, db :Session = Depends(get_db)):
    db_product = db.query(Db_model.Product).filter(Db_model.Product.id == id).first()

    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity

        db.commit()

        return "Product updated......!"
    else:
        return "Product is not Found"


@app.delete("/product/{id}")
def delete_Product(id:int, db :Session = Depends(get_db)):
    db_product = db.query(Db_model.Product).filter(Db_model.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()

        return "Product deleted....!"
    else:
        return "Product Not Found"

# @app.get("/get")
# def test_post(db : Session = Depends(get_db)):
#     return {"Status ": "Success"}