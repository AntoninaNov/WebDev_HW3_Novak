import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from helpers.url_parser import parse_url
from helpers.file_handler import serve_image
from helpers.text_analyzer import analyze_text
import cgi
import json


class SimpleHandler(SimpleHTTPRequestHandler):
    def _send_response(self, message, status=200, content_type='text/html'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        if content_type == 'application/json':
            # Convert JSON to bytes and send
            self.wfile.write(bytes(json.dumps(message), 'utf-8'))
        elif content_type in ['image/jpeg', 'image/png']:
            # Send binary data as-is (for images)
            self.wfile.write(message)
        else:
            # Convert other types to bytes and send
            self.wfile.write(bytes(message, 'utf-8'))

    def do_GET(self):
        print(self.path)

        # Serve Swagger UI
        if self.path in ['/', '/swagger']:
            self.path = '/swagger_ui/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        # Serve Swagger YAML
        if self.path == '/swagger.yaml':
            self.path = '/swagger_ui/swagger.yaml'
            self.send_response(200)
            self.send_header('Content-type', 'application/x-yaml')
            self.end_headers()
            with open(self.path[1:], 'rb') as file:
                self.wfile.write(file.read())
            return

        # Serve Swagger UI assets
        if self.path.startswith('/swagger_ui/'):
            return SimpleHTTPRequestHandler.do_GET(self)

        if self.path.startswith('/parse-url?'):
            query_string = self.path.split('?', 1)[1]
            url = parse_qs(query_string).get('url', [''])[0]
            try:
                response_data = parse_url(url)
                self._send_response(response_data, content_type='application/json')
            except ValueError as e:
                self._send_response({'error': str(e)}, status=400, content_type='application/json')
            return

        if self.path.startswith('/images/'):
            image_path = os.path.join('.', 'assets', 'images', self.path[8:])
            try:
                file_content, content_type = serve_image(image_path)
                self._send_response(file_content, content_type=content_type)
            except FileNotFoundError as e:
                self._send_response({'message': str(e)}, status=404, content_type='application/json')
            return
        else:
            self._send_response({'message': 'Not found'}, status=404)

    def do_POST(self):
        if self.path == '/analyze-text':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
            )
            try:
                if 'file' in form and 'string' in form:
                    file_content = form['file'].file.read().decode('utf-8')
                    search_string = form['string'].value

                    response_data = analyze_text(file_content, search_string)
                    self._send_response(response_data, content_type='application/json')
                else:
                    raise ValueError("Missing file or string in the request")
            except Exception as e:
                self._send_response({'error': str(e)}, status=400, content_type='application/json')


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f'Starting server on port {port}')
    httpd.serve_forever()


run_server()
