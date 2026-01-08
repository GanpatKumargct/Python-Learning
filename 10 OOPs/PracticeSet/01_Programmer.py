
class  programmer:

    company_name = "Microsoft"

    def __init__(self, name, age, salarly):
        self.name = name
        self.age = age 
        self.salarly = salarly


print("Programmer list")

prog = programmer("Gannn",55,1200)
print(prog.company_name)
print(prog.name)
print(prog.age)
print(prog.salarly)