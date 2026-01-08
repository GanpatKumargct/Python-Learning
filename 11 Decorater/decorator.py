

def chipkauuaa(func):
    def wrapper(*args, **kwargs):

        print("This is a chipkauua method.....")
        result = func(*args, **kwargs)

        print(f"The {func.__name__} method is calling with args {args} and kwargs {kwargs}")
        return result
    return wrapper


@chipkauuaa
def hello(name, age=13):
    print(f"Hello {name} {age}, this is for testing method")


hello("gam",age=45)