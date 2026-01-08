
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} ran in {end-start}")

        return result
    return wrapper

@timer
def exampleMethod(n):
    time.sleep(n)


exampleMethod(5)