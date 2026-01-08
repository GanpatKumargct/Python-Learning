
try:
    a = int(input("Enter a number : "))
    print(a)
except Exception as e:
    print(e)


try:
    a=10
    b=a/0
    print(b)
except ZeroDivisionError as z:
    print(z)
except TypeError as t:
    print(t)
except Exception as e:
    print(e)