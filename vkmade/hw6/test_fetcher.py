import unittest
from unittest import mock, IsolatedAsyncioTestCase
import url_maker
from fetcher import fetch_url, main
import aiohttp
import asyncio

class TestFetch(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.path = url_maker.PATH
        self.n_links = url_maker.N_LINKS

    def test_fetch_url_results(self):
        with mock.patch("fetcher.aiohttp.ClientSession.get") as m_get:
            TEST_WORKERS = self.n_links // 1
            TEST_PATH = self.path
            m_get.return_value = mock.Mock(read="some data", status="200")
            mock.call(f"asyncio.run(main({TEST_PATH}, {TEST_WORKERS}))")
    
    @mock.patch("fetcher.aiohttp.ClientSession.get")
    def test_fetch_url_results_side(self, m_get):
        TEST_WORKERS = self.n_links // 1
        TEST_PATH = self.path
        m_get.return_value = mock.AsyncMock(read="some data", status=200)
        asyncio.run(main(TEST_PATH, TEST_WORKERS))


if __name__ == '__main__':
    unittest.main()




