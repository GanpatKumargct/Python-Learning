class Car:

    # Constructor --  and self = this
    def __init__(self, model, brand):
        self.model = model
        self.brand = brand

    def full_name(self):
        return f"{self.model} {self.brand}"



class ElectricCar(Car):
    def __init__(self, model, brand, battery_size):
        super().__init__(model, brand)
        self.battery_size = battery_size


# Object
mycar = ElectricCar("toyota","maruti", "80kwh")
print(mycar.model)
print(mycar.brand)
print(mycar.battery_size)
print(mycar.full_name())