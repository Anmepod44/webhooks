from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def greet():
    return "Marvin made some changes at 16:43pm"

def feature_by_marvin():
    return "This feature was made by marvin"

    return "Hello From Marvin"

def feature_by_dev():
    return "dev made some changes here"