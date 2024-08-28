from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def greet():
    return "Hello From Marvin marvin made some changes"