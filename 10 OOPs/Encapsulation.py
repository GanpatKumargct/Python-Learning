class Car:

    # Constructor --  and self = this
    def __init__(self, model, brand):
        self.__model = model       # __ under score ka matalb hota hai yaha ki attributes is private
        self.__brand = brand

    def full_name(self):
        return f"{self.__model} {self.__brand}"
    
    def get_model(self):
        return self.__model + " !"


    def get_brand(self):
        return f"{self.__brand} this is a private brand"

class ElectricCar(Car):
    def __init__(self, model, brand, battery_size):
        super().__init__(model, brand)
        self.battery_size = battery_size


# Object
mycar = ElectricCar("toyota","maruti", "80kwh")
print(mycar.get_model())
print(mycar.get_brand())
print(mycar.battery_size)
print(mycar.full_name())