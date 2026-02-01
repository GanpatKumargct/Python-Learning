

# class and object
# 1
class Student:
    def display(self):
        print("Hello Student")

s = Student()
s.display()

# 2
class Car:
    def start(self):
        print("Car started")

c = Car()
c.start()

# 3
class Mobile:
    def call(self):
        print("Calling...")

m = Mobile()
m.call()

# 4
class Person:
    def greet(self):
        print("Hello")

p1 = Person()
p2 = Person()

p1.greet()
p2.greet()


# Constructor 
# 1
class Student:
    def __init__(self, name):
        self.name = name

s = Student("Rahul")
print(s.name)


# 2
class Car:
    def __init__(self, brand):
        self.brand = brand

c = Car("Toyota")
print(c.brand)


# 3
class Book:
    def __init__(self, title, price):
        self.title = title
        self.price = price

b = Book("Python Basics", 399)
print(b.title, b.price)


# 4
class Mobile:
    def __init__(self, model):
        self.model = model

m = Mobile("iPhone 14")
print(m.model)



