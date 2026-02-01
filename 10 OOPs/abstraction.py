
from abc import ABC, abstractmethod

class bankApp(ABC):

    def greet(self):
        print("Welcome to the bank")

    @abstractmethod
    def security(self):
        pass

class mobileApp(bankApp):
    
    def display(self):
        print("Something welcome to the sbi bank")

    # def security(self):
    #     print("We had a heavy security")


mob = mobileApp()
mob.display()
