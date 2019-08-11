import asyncio
from aiohttp import ClientSession


async def fetch(semaphore, url, session):
    async with semaphore:
        async with session.get(url) as response:
            return await response.text()


async def crawl(urls, results, semaphore=None):
    semaphore = semaphore or asyncio.Semaphore(1)
    async with ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(semaphore=semaphore, url=url, session=session)) for url in urls]
        responses = asyncio.gather(*tasks)
        await responses
        results.extend(responses.result())


def run(urls, limit=100, loop=None):
    loop = loop or asyncio.get_event_loop()
    results = []

    coroutine = crawl(urls=urls, results=results, semaphore=asyncio.Semaphore(limit))
    loop.run_until_complete(asyncio.ensure_future(coroutine))

    return results
