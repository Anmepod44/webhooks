from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def greet():
    return "Marvin made some changes at 16:43pm"