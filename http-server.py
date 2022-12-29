import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
import datetime

PORT = 8000

#Handler = http.server.SimpleHTTPRequestHandler

class myHandler(SimpleHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):

      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      # Send the html message
      self.wfile.write(bytes("<b> Hello World !</b>"
                       + "<br><br>Current time and date: " + str(datetime.datetime.now()), 'utf-8'))

# with socketserver.TCPServer(("", PORT), myHandler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()
def run(server_class=HTTPServer, handler_class=myHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()