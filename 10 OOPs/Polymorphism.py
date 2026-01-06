
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
    
    def fuel_type(self):
        return "disel or petrol"

class ElectricCar(Car):
    def __init__(self, model, brand, battery_size):
        super().__init__(model, brand)
        self.battery_size = battery_size

    def fuel_type(self):
        return "Battery charge"
    
    # def fuel_type(self, battery_Type):
    #     return f"This is a Electric vehicle with {battery_Type} battery."
    
safari = Car("Safari","Tata")
print(safari.fuel_type())

suv = ElectricCar("SUV", "Tata", "70kwh")
print(suv.fuel_type())
# print(suv.fuel_type("DC"))
