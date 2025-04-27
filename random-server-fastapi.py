from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import os
import json
import uvicorn

# File to store our used random numbers
PERSISTENCE_FILE = "used_numbers.json"

# Define response model
class RandomNumberResponse(BaseModel):
    number: int

# Create FastAPI app
app = FastAPI(title="Unique Random Number Server With FastAPI")

# Define the range for our random numbers
MIN_NUM = 100
MAX_NUM = 100000

# Load the set of previously used numbers
def get_used_numbers():
    if os.path.exists(PERSISTENCE_FILE):
        with open(PERSISTENCE_FILE, 'r') as f:
            return set(json.load(f))
    return set()

# Save the updated set of used numbers
def save_used_numbers(used_numbers):
    with open(PERSISTENCE_FILE, 'w') as f:
        json.dump(list(used_numbers), f)

# Define the endpoint
@app.get("/random", response_model=RandomNumberResponse)
def get_random_number():
    used_numbers = get_used_numbers()
    
    # If we've used all possible numbers in our range
    if len(used_numbers) >= (MAX_NUM - MIN_NUM + 1):
        raise HTTPException(
            status_code=503,
            detail="All possible numbers have been used"
        )
    
    # Generate random numbers until we find a new one
    while True:
        new_number = random.randint(MIN_NUM, MAX_NUM)
        if new_number not in used_numbers:
            used_numbers.add(new_number)
            save_used_numbers(used_numbers)
            return {"number": new_number}

# Handle 404 errors for other paths
@app.get("/{path:path}")
def not_found(path: str):
    raise HTTPException(status_code=404, detail="Not found")

# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)