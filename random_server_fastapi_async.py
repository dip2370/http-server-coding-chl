from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import time
from typing import Union
import random

app = FastAPI()

DB_FILE = "random_numbers.db"

# Setup database and table
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")  # Enable better concurrency
    conn.execute("""
        CREATE TABLE IF NOT EXISTS random_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number REAL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

init_db()

# Pydantic model for response
class RandomNumberResponse(BaseModel):
    number: Union[int, float]

def generate_random_number(is_float: bool = False) -> Union[int, float]:
    if is_float:
        return round(random.uniform(0, 1e8), 6)  # 6 decimal places
    else:
        return random.getrandbits(32)

def insert_number(number: Union[int, float]) -> bool:
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("INSERT INTO random_numbers (number) VALUES (?);", (number,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

@app.get("/random", response_model=RandomNumberResponse)
async def get_random_number(type: str = "int"):
    is_float = type == "float"
    
    max_attempts = 5
    for _ in range(max_attempts):
        number = generate_random_number(is_float=is_float)
        if insert_number(number):
            return {"number": number}
        time.sleep(0.01)  # tiny sleep to avoid hammering in retry

    raise HTTPException(status_code=503, detail="Could not generate unique random number after retries.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)