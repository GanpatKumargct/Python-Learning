
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

class vehicle(BaseModel):
    id:int
    name : str
    model : int
    isRunning : bool = True
    color : Optional[str] = None

app = FastAPI()

vehicles = [
    {
        "id": 1,
        "name": "Honda",
        "model": 2022,
        "isRunning": True,
        "color": "Red"
    },
    {
        "id": 2,
        "name": "Toyota",
        "model": 2020,
        "isRunning": False,
        "color": None
    },
    {
        "id": 3,
        "name": "Tesla",
        "model": 2024,
        "isRunning": True,
        "color": "White"
    }
]


def find_vehicle(id):
    for p in vehicles:
        if p["id"]==id:
            return p

@app.get("/vehicle")
def getVehicle():
    return {"data":vehicles}

@app.get("/vehicle/{id}")
def getvehiclebyid(id):
    print(type(id))
    vech = find_vehicle(int(id))
    return {"data":vech}

@app.post("/")
def postvehicle(car : vehicle):
    print(car.isRunning)

    # vech_dict = car.dict()
    # # car.id = randrange(5,100)
    # vech_dict['id'] = randrange(5,10000)
    vehicles.append(car)
    return {"message": "successfuly done",
            "data":car}


