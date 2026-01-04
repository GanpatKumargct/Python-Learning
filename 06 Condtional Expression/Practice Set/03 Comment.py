c1 = "Make a lot of money"
c2 = "buy now"
c3 = "subscribe this"
c4 = "click this"

message = input("Enter the Message : ")

if((c1 in message) or (c2 in message) or (c3 in message) or (c4 in message)):
    print("This Message is a Spam..!")
else:
    print("This message not a spam...!")