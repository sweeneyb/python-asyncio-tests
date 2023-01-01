# ASYNCIO tests

A small repo where I learn some python and libraries to demo some asnyc concepts.

## Why?
I have a server that can only handle so much load at a time. It needs to exert some back pressure, and I wanted to think through how to implement that client side.  I need to implement it in a language I'm not familiar with, so easier to write it in python, then convert.

## Sync client
Easier than expected.  On each loop, wait for some interval.  The interval will decrease by 25% when it sees a 200 (really, most responses).  When a 429 is seen, increase the interval by 2x + some jitter.  Inspired by TCP window scaling.

## Queue server
More difficult than I expected.  I needed a mock.  But the doc on running an async web server with a queue consumer was light.  

I was having trouble getting a sync web handler from the std lib to see items placed into the asyncio queue.  I suspect that was due to threading issues I don't understand within python.  I got a pointer to switch to aiohttp so that I could use the async methods on the async queue.  In reality, I think the benefit was putting the server and the consumer on the same event loop (ie, same thread. This feels like node.)

The other detail I had trouble finding in doc is:

```
task = web.run_app(app , loop = loop)
```
1. run_app() is often shown with an app, but doesn't often specify a loop.  By default, it creates a new loop.
1. run_app() invokes "run_until_complete()" on that loop.

The net result is, in order to have a consumer eat things from a queue, its task needs to be set up and scheduled on the event loop before run_app() is invoked.  

But then, everything works.  And an item is consumed from the queue every 5 seconds (because I have a static 5 second sleep, 1 reader, and it's sync within the loop).