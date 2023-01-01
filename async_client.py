import aiohttp
import asyncio
import requests

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())