import aiohttp
import asyncio
import time
import sys
import argparse

DEFAULT_WORKERS = 50

async def fetch_url(url, session):
    print(1)
    async with session.get(url) as resp:
        data = await resp.read()
        print(resp.status, len(data))

        return len(data) 
    print(2)


async def worker(queue, session):
    while True:
        url = await queue.get()
        try:
            res = await fetch_url(url, session)
        finally:
            queue.task_done()


async def fetch_batch_urls(queue, workers):
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(worker(queue, session))
            for i in range(workers)
        ]

        await queue.join()
        for task in tasks:
            task.cancel()


async def main(filepath, workers):
    with open(filepath, 'r') as f:
        urls_queue = asyncio.Queue()
        for new_url in f:
            await urls_queue.put(new_url)
        await fetch_batch_urls(urls_queue, workers)


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-c', '--count', nargs=1, default=DEFAULT_WORKERS, type=int, required=True)
    parser.add_argument('filepath')
    parser.add_argument('-t', '--time', action='store_const', const=True)
 
    return parser


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    filepath = namespace.filepath
    WORKERS = namespace.count[0]


    if namespace.time:
        t1 = time.time()

    asyncio.run(main(filepath, WORKERS))

    if namespace.time:
        print(time.time() - t1)


