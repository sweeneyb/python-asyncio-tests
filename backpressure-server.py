import asyncio
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
import datetime
import time
import os
import random
import threading
import _thread

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

async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        time.sleep(4)
        try:
          i, t = q.get_nowait()
          now = time.perf_counter()
          print(f"Consumer {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")
          q.task_done()
        except:
          print("nothing in queue")

async def consume_async(name: int, q: asyncio.Queue) -> None:
        #await randsleep(caller=f"Consumer {name}") 
        print(f"Consumer {name} about to wait")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")
        q.task_done()

t = threading.Thread(target=run)
t.start()
# _thread.start_new_thread(run)
print("serving...")
loop = asyncio.get_event_loop()
loop.create_task(consume(1,q)) 
# loop.create_task(consume_async(1,q))
loop.run_forever()

