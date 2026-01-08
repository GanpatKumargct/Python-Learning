from random import randint

class Train:

    def __init__(self, TrainNo, From, TO):
        self.TrainNo = TrainNo
        self.From = From
        self.TO = TO


    def bookTicket(self):
        print(f"The ticket is successfully booked from {self.From} to {self.TO} in Train No {self.TrainNo}")

    def getStatus(self):
       print(f"The Train No {self.TrainNo} is delayed by 1 hours...!")

    def getFare(self):
        print(f"The TrainNO {self.TrainNo} is from {self.From} to {self.TO} of fare is {self.randint(222,5565)}")


train  = Train(12230, "CSMT", "Patna")
train.bookTicket()
train.getStatus()
train.getFare()