# Http Server to host video streams

from http.server import SimpleHTTPRequestHandler

class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    from http.server import HTTPServer
    import sys

    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSHTTPRequestHandler)

    print(f'Starting CORS-enabled server on port {port}...')
    httpd.serve_forever()
