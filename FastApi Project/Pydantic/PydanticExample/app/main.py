
from typing import Optional
from fastapi import FastAPI , Response, status, HTTPException
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


@app.get("/vehicle/latest")
def getsomething():
    return "Something in the car....!"

@app.get("/vehicle/{id}")
def getvehiclebyid(id :int, res : Response):
    print(type(id))
    vech = find_vehicle(id)
    if not vech:
        # res.status_code =status.HTTP_404_NOT_FOUND
        # return {"message":f"the {id} value is not found."}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the {id} value is not found.")
    return {"data":vech}


@app.post("/",status_code=status.HTTP_201_CREATED)
def postvehicle(car : vehicle):
    print(car.isRunning)


    vehicles.append(car)
    return {"message": "successfuly done",
            "data":car}


# chat gpt code
@app.put("/vehicle/{id}")
def update_vehicle(id: int, updated_car: vehicle):
    for index, v in enumerate(vehicles):
        if v["id"] == id:
            vehicles[index] = updated_car.dict()
            vehicles[index]["id"] = id  # keep same id
            return {"message": "vehicle updated", "data": vehicles[index]}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"vehicle with id {id} not found"
    )


@app.delete("/vehicle/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(id: int):
    for index, v in enumerate(vehicles):
        if v["id"] == id:
            vehicles.pop(index)
            return {"message": "Deleted SuccessFully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"vehicle with id {id} not found"
    )

    return {"message": "Deleted SuccessFully"}
