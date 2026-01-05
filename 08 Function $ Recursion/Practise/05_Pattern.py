
def star(n):
    for i in range(3,0,-1):
        print("*"*i)

star(3)


def StarRecursive(n):
    if(n==0):
        return
    
    print("*"*n)
    StarRecursive(n-1)

StarRecursive(5)