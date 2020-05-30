import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return (await response.text())