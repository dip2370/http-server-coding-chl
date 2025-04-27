from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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

# Add a root route with welcome message
@app.get("/", response_class=HTMLResponse)
def welcome():
    return """
    <html>
        <head>
            <title>Unique Random Number Server</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    text-align: center;
                }
                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to Unique Random Number Server With FastAPI</h1>
            <p>Click below to get a unique random number:</p>
            <a href="/random">Get Random Number</a>
        </body>
    </html>
    """

# Modify the random endpoint to return HTML
@app.get("/random", response_class=HTMLResponse)
def get_random_number_html():
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
            
            # Return HTML response with the number
            return f"""
            <html>
                <head>
                    <title>Your Random Number</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 40px;
                            text-align: center;
                        }}
                        .number {{
                            font-size: 24px;
                            font-weight: bold;
                            color: #4CAF50;
                            margin: 20px 0;
                        }}
                        a {{
                            display: inline-block;
                            margin: 10px;
                            padding: 10px 20px;
                            background-color: #4CAF50;
                            color: white;
                            text-decoration: none;
                            border-radius: 4px;
                        }}
                    </style>
                </head>
                <body>
                    <h1>Welcome to Unique Random Number Server With FastAPI</h1>
                    <p>The random number is...</p>
                    <div class="number">{new_number}</div>
                    <a href="/random">Get Another Number</a>
                    <a href="/">Home</a>
                </body>
            </html>
            """

# Add JSON API endpoint to maintain compatibility
@app.get("/api/random", response_model=RandomNumberResponse)
def get_random_number_json():
    used_numbers = get_used_numbers()
    
    if len(used_numbers) >= (MAX_NUM - MIN_NUM + 1):
        raise HTTPException(
            status_code=503,
            detail="All possible numbers have been used"
        )
    
    while True:
        new_number = random.randint(MIN_NUM, MAX_NUM)
        if new_number not in used_numbers:
            used_numbers.add(new_number)
            save_used_numbers(used_numbers)
            return {"number": new_number}

# Handle 404 errors for other paths
@app.get("/{path:path}")
def not_found(path: str):
    if path.startswith("api/"):
        # Return JSON for API routes
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Return HTML for web routes
    return HTMLResponse(content="""
    <html>
        <head>
            <title>Page Not Found</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    text-align: center;
                }
                h1 { color: #d9534f; }
                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <h1>404 - Page Not Found</h1>
            <p>The page you're looking for doesn't exist.</p>
            <a href="/">Return to Home</a>
        </body>
    </html>
    """, status_code=404)

# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)