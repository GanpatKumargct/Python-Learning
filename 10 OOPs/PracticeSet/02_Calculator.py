
class Calculator:

    def __init__(self):
        pass

    @staticmethod
    def hello():
        print("Heloo everyone...!")

    def squareRooot(self, num):
        return num**(1/2)
    
    def squareCube(self, num):
        return num**3
    

cal = Calculator()

sq = cal.squareCube(5)
sq2 = cal.squareRooot(16)
cal.hello()

print(f"Square Cube {sq} and Square Root {sq2}")