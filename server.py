from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs
import ocrmypdf
import json
import sys
import tempfile
import traceback

def makeHandler():
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                query = parse_qs(urlparse(self.path).query)
                def query_string(name, default):
                    raw = query.get(name, [])
                    if len(raw) == 1:
                        return raw[0]
                    else:
                        return default
                def query_boolean(name, default):
                    raw = query.get(name, [])
                    if len(raw) == 1 and (raw[0] == 'yes' or raw[0] == 'true' or raw[0] == '1'):
                        return True
                    elif len(raw) == 1 and (raw[0] == 'no' or raw[0] == 'false' or raw[0] == '0'):
                        return False
                    else:
                        return default

                with tempfile.NamedTemporaryFile() as temp:
                    with tempfile.NamedTemporaryFile() as tempOut:
                        temp.write(post_data)
                        temp.seek(0)

                        result = ocrmypdf.ocr(
                            temp.name,
                            tempOut.name,
                            language = 'deu+eng',
                            rotate_pages = query_boolean('rotate_pages', True),
                            deskew = query_boolean('deskew', True),
                            remove_background = query_boolean('remove_background', True),
                            clean_final = True,
                            force_ocr = query_boolean('force_ocr', False),
                            unpaper_args = '--dpi %s --post-size a4' % query_string('dpi', '200'),
                            progress_bar = False
                        )

                        self.send_response(200)
                        self.send_header('Content-type', 'application/pdf')
                        self.end_headers()
                        self.wfile.write(tempOut.read())
            except ocrmypdf.exceptions.PriorOcrFoundError:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes('Document already has been OCRed', 'utf-8')) 
            except:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes('Unknown error', 'utf-8'))
                traceback.print_exc(file=sys.stdout)

    return Handler

def run(port=8080):
    httpd = HTTPServer(('', port), makeHandler())
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        run(port = int(argv[1]))
    else:
        run()
