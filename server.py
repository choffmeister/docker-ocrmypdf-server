from http.server import BaseHTTPRequestHandler, HTTPServer
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

                with tempfile.NamedTemporaryFile() as temp:
                    with tempfile.NamedTemporaryFile() as tempOut:
                        temp.write(post_data)
                        temp.seek(0)


                        result = ocrmypdf.ocr(
                            temp.name,
                            tempOut.name,
                            language='deu+eng',
                            deskew=True,
                            clean_final=True,
                            rotate_pages=True,
                            unpaper_args='--post-size a4',
                            remove_background=True,
                            progress_bar=False
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
        run(port=int(argv[1]))
    else:
        run() 