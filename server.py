from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class CustomHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _handle_request(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length else None

        response = {
            "method": self.command,
            "path": self.path,
            "headers": dict(self.headers),
            "body": body,
            "message": "Request received successfully!"
        }

        print(f"Received {self.command} request for {self.path}")
        print(f"Headers: {self.headers}")
        print(f"Body: {body}")

        self._set_headers()
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))

    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def do_PUT(self):
        self._handle_request()

    def do_DELETE(self):
        self._handle_request()

def run(server_class=HTTPServer, handler_class=CustomHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving HTTP on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
