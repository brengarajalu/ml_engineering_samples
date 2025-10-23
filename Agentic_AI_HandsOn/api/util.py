import aiofiles
import asyncio
import json

import aiohttp


async def read_file_async(file_name):
    async with aiofiles.open(file_name, 'r') as file:
        content = await file.read()
        return content

async def write_to_file_async(file_name, data):
    async with aiofiles.open(file_name, 'w') as file:
        await file.write(data)
        print(f"Data written to {file_name}"

async def read_file():
    content = await read_file_async('example.txt')
    print(content)

async def write_to_file():
    content = await write_to_file_async('example.txt', 'Hello, async world!')
    print(content)


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    url = 'http://example.com'
    data = await fetch(url)
    print(data)

asyncio.run(main())