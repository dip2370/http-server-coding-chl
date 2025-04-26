from http.server import HTTPServer, BaseHTTPRequestHandler

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        # Write response body
        self.wfile.write(b'Hello, world!')

def run(server_class=HTTPServer, handler_class=HelloHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving HTTP on port {port} (http://localhost:{port}/) …')
    httpd.serve_forever()

if __name__ == '__main__':
    run()