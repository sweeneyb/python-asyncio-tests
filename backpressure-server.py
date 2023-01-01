import asyncio
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
import datetime
import time
import os
import random
import threading
import _thread
from aiohttp import web

PORT = 8000

q = asyncio.Queue()


def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


class myHandler(SimpleHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        i = makeitem()
        t = time.perf_counter()
        q.put_nowait((i, t))
        print(f"added to queue and size is now {q.qsize()}")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(bytes(f"<b> Hello World !</b>"
                         + "<br><br>Current time and date: " + str(datetime.datetime.now())+ " queue size: " + str(q.qsize()), 'utf-8'))

def run(server_class=HTTPServer, handler_class=myHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


async def randsleep(caller=None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)

async def consume_async(name: int, q: asyncio.Queue) -> None:
    while True:
        #await randsleep(caller=f"Consumer {name}") 
        print(f"Consumer_async {name} about to wait")
        i, t = await q.get()
        now = time.perf_counter()
        await asyncio.sleep(5)
        print(f"Consumer {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")
        q.task_done()


async def handle(request):
    if(str(request.url).endswith('favicon.ico')):
        return web.Response(status=404)
    if(q.qsize() > 3):
        return web.Response(status=429)
    print(request.url)
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name + ", queue size: " + str(q.qsize())
    i = makeitem()
    t = time.perf_counter()
    await q.put((i, t))
    print(f"added to queue and size is now {q.qsize()}")
    return web.Response(text=text)

loop = asyncio.get_event_loop()
loop.create_task(consume_async(1,q)) 

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

# This runs until completion, so schedule all of your coroutines for the loop above
task = web.run_app(app , loop = loop)
print("serving...")


