import unittest
from unittest import mock, IsolatedAsyncioTestCase
import url_maker
from fetcher import fetch_url, main
import aiohttp
import asyncio

class AsyncContextManager:
    def __init__(self, readable_content="some data"):
        self.status = 200
        self.text = readable_content
    async def __aenter__(self):
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(0.1)

    async def read(self):
        await asyncio.sleep(0.1)
        return self.text

def side_effect_func(url="some url"):
    return url

class TestFetch(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.path = url_maker.PATH
        self.n_links = url_maker.N_LINKS
        self.cntxt = AsyncContextManager(readable_content="data")
        self.read_len =  len(self.cntxt.text)
    
    @mock.patch("fetcher.aiohttp.ClientSession.get")
    def test_fetch_url_results_two_workers(self, m_get):
        TEST_WORKERS = 2
        TEST_PATH = self.path
        m_get.return_value = self.cntxt

        asyncio.get_event_loop().run_until_complete(main(TEST_PATH, TEST_WORKERS))
    
if __name__ == '__main__':
    unittest.main()




