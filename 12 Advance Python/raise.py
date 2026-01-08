

a = int(input("Emter a number : "))
b = int(input("Emter a number : "))

if(b==0):
    raise ZeroDivisionError("The number can't be divisble by 0")

print(f"zero divisble {a/b}")