from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio
import socketserver
import threading
import io
from ClockController import Clock

hostName = "localhost"
serverPort = 8080
clock = Clock()
stop_requested = False

class MyHTTPServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            try:
                content = open('html/index.html', 'r').read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
            except:
                self.send_response(500)

        elif self.path == '/stop':
            try:

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("Stopping...", "utf-8"))
            except:
                self.send_response(500)

        elif self.path == '/latest.jpg':
            try:
                content = open('html/latest.jpg', 'rb').read()
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.end_headers()
                self.wfile.write(content)
            except:
                self.send_response(500)
        else:
            self.send_response(404)

# async def tick_async(server):
#     while True:
#         await asyncio.sleep(1.0)

def start_server():
    httpd.serve_forever()
    
def start_clock():
    clock.start()
    
if __name__ == '__main__':
    httpd = HTTPServer(('', 8080), MyHTTPServer)
    # asyncio.ensure_future(tick_async(httpd))
    loop = asyncio.get_event_loop()
    tHttpd = threading.Thread(target=start_server)
    tHttpd.start()
    tClock = threading.Thread(target=start_clock)
    tClock.start()
    loop.run_forever()
