from fastapi import FastAPI
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

#Set up templates directory.
templates=Jinja2Templates(directory=r"./templates")

app=FastAPI()

@app.get("/")
def greet():
    return "Marvin made some changes at 16:43pm"

@app.get("/hello")
def hello(request:Request):
    return templates.TemplateResponse('index.html',{'request':request})

@app.post("/hook")
def hook(data:dict):
    print(f" Received a payload from github hook of action {data['action']} at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}")
    return "Received"

def feature_by_marvin():
    return "This feature was made by marvin"

def feature_by_dev():
    return "dev raised a conflict with the main, that requires resolution."

def conflict_by_dev():
    return "This is a conflict by dev"