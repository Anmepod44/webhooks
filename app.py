from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def greet():
    return "Hello From Marvin"

def feature_by_dev():
    return "dev made some changes here"