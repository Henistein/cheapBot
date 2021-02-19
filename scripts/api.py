from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import json

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "cheapBot API"}

@app.get("/approval")
async def approval():
  with open("approval.json", "r") as openfile:
    data = json.load(openfile)              
  return data
