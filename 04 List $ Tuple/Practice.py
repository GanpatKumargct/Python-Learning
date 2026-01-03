# 01

list = []
print(list)

f1 = input("Enter the fruit name : ")
f2 = input("Enter the fruit name : ")
f3 = input("Enter the fruit name : ")
f4 = input("Enter the fruit name : ")
f5 = input("Enter the fruit name : ")
list.append(f1)
list.append(f2)
list.append(f3)
list.append(f4)
list.append(f5)

print(list)

# 02

mark = []

stud1 = int(input("Enter your marks "))
mark.append(stud1)

stud2 = int(input("Enter your marks "))
mark.append(stud2)

stud3 = int(input("Enter your marks "))
mark.append(stud3)

stud4 = int(input("Enter your marks "))
mark.append(stud4)

stud5 = int(input("Enter your marks "))
mark.append(stud5)

mark.sort()

print(mark)


# 03

tuple = (4,56,8,2,1)
# tuple[1] = 5   # can't change -- Error
print(tuple)

# 04

listSum = [1,5,6,2,4]
print(sum(listSum))


# 05
a = (7, 0, 8, 0, 0, 9)
print(a.count(0))