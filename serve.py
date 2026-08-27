import os, http.server, socketserver
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 8787
httpd = socketserver.TCPServer(('', PORT), http.server.SimpleHTTPRequestHandler)
print(f'Serving at http://localhost:{PORT}')
httpd.serve_forever()
