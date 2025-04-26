from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
import os

# File to store our used random numbers
PERSISTENCE_FILE = "used_numbers.json"

class RandomNumberHandler(BaseHTTPRequestHandler):
    # Load the set of previously used numbers
    def get_used_numbers(self):
        if os.path.exists(PERSISTENCE_FILE):
            with open(PERSISTENCE_FILE, 'r') as f:
                return set(json.load(f))
        return set()
    
    # Save the updated set of used numbers
    def save_used_numbers(self, used_numbers):
        with open(PERSISTENCE_FILE, 'w') as f:
            json.dump(list(used_numbers), f)
    
    # Generate a new unique random number
    def generate_unique_random(self):
        used_numbers = self.get_used_numbers()
        
        # Define the range for our random numbers
        MIN_NUM = 100
        MAX_NUM = 100000
        
        # If we've used all possible numbers in our range
        if len(used_numbers) >= (MAX_NUM - MIN_NUM + 1):
            self.send_response(503)  # Service Unavailable
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "All possible numbers have been used"}).encode())
            return None
        
        # Generate random numbers until we find a new one
        while True:
            new_number = random.randint(MIN_NUM, MAX_NUM)
            if new_number not in used_numbers:
                used_numbers.add(new_number)
                self.save_used_numbers(used_numbers)
                return new_number
    
    def do_GET(self):
        if self.path == '/random':
            # Generate a unique random number
            random_number = self.generate_unique_random()
            
            # If we couldn't generate a number
            if random_number is None:
                return
            
            # Send successful response with the random number
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"number": random_number}
            self.wfile.write(json.dumps(response).encode())
        else:
            # Handle other paths with a 404 Not Found
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())

def run(server_class=HTTPServer, handler_class=RandomNumberHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving HTTP on port {port} (http://localhost:{port}/) ...')
    print(f'Try accessing http://localhost:{port}/random to get a random number')
    httpd.serve_forever()

if __name__ == '__main__':
    run()