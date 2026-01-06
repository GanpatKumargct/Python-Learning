
# Reading a file
f = open("file.txt",'r')
data = f.read()
print(data)
f.close()


# Write a file

st = "Eye is to beautiful Than you can see beautiful world"
file = open("file.txt",'a')
file.write(st)
file.close