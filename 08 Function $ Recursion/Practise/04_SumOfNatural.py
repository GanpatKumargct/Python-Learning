
def Sum(n):
    if n==1:
        return 1
    else:
        return n+Sum(n-1)
    
add = Sum(5)
printf(f"Sum is {add}")