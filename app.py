from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def greet():
    return "Hello From Marvin some changes were made by dev"