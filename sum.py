from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/add")
def add_num(numbers: Dict[str, int]):
    a = numbers.get("a")
    b = numbers.get("b")
    return {"sum": a + b}
