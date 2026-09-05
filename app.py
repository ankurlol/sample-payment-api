import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Change this to "v2.0.0-broken" to simulate a bad release
VERSION = os.getenv("APP_VERSION", "v1.0.0-stable")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "version": VERSION}).encode())
        elif self.path == "/api/pay":
            if "broken" in VERSION:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "KeyError: 'tier' in payment.py:42"}).encode())
            else:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "payment_processed", "version": VERSION}).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(f"<h1>Payment Service Live: {VERSION}</h1>".encode())

def run():
    port = int(os.getenv("PORT", 3000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"Service running on port {port} (Version: {VERSION})")
    server.serve_forever()

if __name__ == "__main__":
    run()
