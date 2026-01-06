
# Defining a class
class car:

    # Constructor --  and self = this
    def __init__(self, model, brand):
        self.model = model
        self.brand = brand



c = car("2025","Thar")
print(c.brand)
print(c.model)

c2 = car("maruti","suzki")
print(c2.brand)
print(c2.model)