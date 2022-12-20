import unittest
from unittest import mock, IsolatedAsyncioTestCase
import url_maker
from fetcher import fetch_url, main
import aiohttp
import asyncio

def side_effect_func(url="some url"):
    return url

class TestFetch(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.path = url_maker.PATH
        self.n_links = url_maker.N_LINKS

    def test_fetch_url_results(self):
        with mock.patch("fetcher.aiohttp.ClientSession.get") as m_get:
            TEST_WORKERS = self.n_links // 1
            TEST_PATH = self.path
            m_get.return_value = mock.AsyncMock()
            print(m_get.mock_calls)
            asyncio.run(main(TEST_PATH, TEST_WORKERS))
    

    @mock.patch("fetcher.aiohttp.ClientSession.get")
    def test_fetch_url_results_side(self, m_get):
        TEST_WORKERS = self.n_links // 1
        TEST_PATH = self.path
        m_get.return_value = mock.Mock()
        asyncio.run(main(TEST_PATH, TEST_WORKERS))

    # @mock.patch("fetcher.aiohttp.ClientSession.get")
    # @mock.patch("fetcher.fetch_url")
    # def test_fetch_one_url(self, m_get, m_fetch_url):
    #     m_get.return_value = mock.AsyncMock()
    #     m_fetch_url.return_value = 13
    #     result_call = m_fetch_url("some url", "some session")
    #     self.assertEqual(result_call, 13)

    # @mock.patch("fetcher.aiohttp.ClientSession.get")
    # @mock.patch("fetcher.fetch_url")
    # def test_fetch_three_url(self, m_get, m_fetch_url):
    #     m_get.return_value = mock.AsyncMock()
    #     m_fetch_url.side_effect = [12, 13, 14]
    #     result_call = [
    #         m_fetch_url("some url1", "some session"),
    #         m_fetch_url("some url2", "some session"),
    #         m_fetch_url("some url3", "some session"),
    #         ]
    #     self.assertEqual(result_call, [12, 13, 14])    
    



if __name__ == '__main__':
    unittest.main()




