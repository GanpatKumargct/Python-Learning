
# Defining a class
class car:

    # Constructor --  and self = this
    def __init__(self, model, brand):
        self.model = model
        self.brand = brand

    def full_name(self):
        return f"{self.model} {self.brand}"


# Object
c = car("2025","Thar")
print(c.brand)
print(c.model)
print(c.full_name())

c2 = car("maruti","suzki")
print(c2.brand)
print(c2.model)
print(c2.full_name())

