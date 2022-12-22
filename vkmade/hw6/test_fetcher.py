import unittest
from unittest import mock, IsolatedAsyncioTestCase
import url_maker
from fetcher import main, worker, QUEUE_MAXSIZE
import asyncio

class AsyncContextManager:
    def __init__(self, content="some data", status=200):
        self.status = status
        self.content = content
    async def __aenter__(self):
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(0.1)

    async def read(self):
        await asyncio.sleep(0.1)
        return self.content

async def side_effect_worker(queue, session):
    while True:
        await queue.get()
        try:
            await asyncio.sleep(0.01)
        finally:
            queue.task_done()

class TestFetch(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.path = url_maker.PATH
        self.n_links = url_maker.N_LINKS
        f = open('print_res.txt', 'w')
        f.close()    
    
    @mock.patch("fetcher.aiohttp.ClientSession.get")
    @mock.patch('builtins.print')
    def test_fetch_url_results_two_workers(self,m_print, m_get):
        TEST_WORKERS = 2
        TEST_PATH = self.path
        content = "data"
        status = 200
        read_len = 4

        self.cntxt = AsyncContextManager(content=content, status=status)
        self.read_len = len(self.cntxt.content)

        m_get.return_value = self.cntxt
        expected = [(status, read_len)] * self.n_links
        asyncio.get_event_loop().run_until_complete(main(TEST_PATH, TEST_WORKERS))
        
        resprint = [i.args for i in m_print.mock_calls]
        self.assertEqual(resprint, expected)
    
    @mock.patch("fetcher.aiohttp.ClientSession.get")
    @mock.patch('builtins.print')
    def test_fetch_url_results_five_workers(self,m_print, m_get):
        TEST_WORKERS = 5
        TEST_PATH = self.path
        content = "lalala"
        status = 200
        read_len = 6

        self.cntxt = AsyncContextManager(content=content, status=status)
        self.read_len = len(self.cntxt.content)

        m_get.return_value = self.cntxt
        expected = [(status, read_len)] * self.n_links
        asyncio.get_event_loop().run_until_complete(main(TEST_PATH, TEST_WORKERS))
        
        resprint = [i.args for i in m_print.mock_calls]
        self.assertEqual(resprint, expected)

    @mock.patch('fetcher.worker')
    def test_workers_created(self, m_worker):
        TEST_WORKERS = 3
        TEST_PATH = self.path

        m_worker.side_effect = side_effect_worker
        asyncio.get_event_loop().run_until_complete(main(TEST_PATH, TEST_WORKERS))
        self.assertEqual(m_worker.call_count, QUEUE_MAXSIZE * TEST_WORKERS)
    
if __name__ == '__main__':
    unittest.main()




