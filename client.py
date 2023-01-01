from time import sleep
import aiohttp
import asyncio
import requests
import random

list = list(range(30))
interval = 1
for i in list:
    print(f"fetch for {i}")
    x = requests.get(f'http://localhost:8080/{i}')
    print(x.status_code)
    if x.status_code == 429:
        list.insert(0,i)
        interval += interval*2 + random.randint(0,1)*interval
        print(f"new expanded interval: {interval}")
    else:
        interval = 0.75*interval
        print(f"new shrinking interval: {interval}")
        print(x.text)
    sleep(interval)
