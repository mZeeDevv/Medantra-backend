from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            "status": "ok",
            "message": "Vision RAG API is running",
            "endpoints": ["/embed-image", "/embed-pdf", "/ask"]
        }
        self.wfile.write(json.dumps(response).encode())
