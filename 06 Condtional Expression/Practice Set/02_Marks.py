
subj1 = int(input("Enter the marks 1"))
subj2 = int(input("Enter the marks 2"))
subj3 = int(input("Enter the marks 3"))

total_marks = (subj1+subj2+subj3)/3

if(total_marks>=40 and subj1>=33 and subj2 >=33 and subj3>=33):
    print("You're passed ",total_marks)
else:
    print("You're a Fail ",total_marks)