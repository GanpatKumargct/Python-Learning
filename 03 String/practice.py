# 01
name = input("Enter Your Name : ")

print(name, " Good Afternoon")
print(f"Good AfterNoon {name}")

# 02
letter = '''
Dear <|Name|>,
You are selected!
<|Date|>
'''

after = letter.replace("<|Name|>", "Ggg").replace("<|Date|>", "02 Januray 2025")
print(after)

#3
line = "This is a  good boy"
print(line.find("  "))

# 4
update = line.replace("  "," ")
print(update)

# 5
letter = "Dear Harry,\n \tthis \'python\' course is nice. Thanks!"
print(letter)