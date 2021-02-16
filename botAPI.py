from fastapi import FastAPI

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
