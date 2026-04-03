from fastapi import FastAPI
from inference import run_inference  # adjust if needed

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/decision")
def decision():
    result = run_inference()  # or whatever your function is
    return {"result": result}