from fastapi import FastAPI
from app.routing import todo
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse 

app = FastAPI()

# Register the all routes here...........
app.include_router(todo.router)

@app.exception_handler(RequestValidationError)
async def valid_exception_handler(request, exc):
    errors = {}
    for error in exc.errors():
        print(f"The error is {error}")
        errors[error["loc"][-1]]=error["msg"]

    return JSONResponse(
        {"message ":"Validation Error", "errors ":errors}, status_code=422
    )




@app.get("/")
def home():
    return "Welcome to Home Page...!"