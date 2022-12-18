import unittest
from unittest import mock, IsolatedAsyncioTestCase
import url_maker
from fetcher import fetch_url
import fetcher

class TestFetch(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.path = url_maker.PATH
        self.n_links = url_maker.N_LINKS

    def test_get_fetch_results(self):
        TEST_WORKERS = self.n_links // 1
        TEST_PATH = self.path
        print(1)
        with mock.patch("fetcher.aiohttp.ClientSession.session.get") as m_get:
            m_get.return_value = mock.Mock(read="some data", status="200")
            mock.call(f"asyncio.run(fetcher.main({TEST_PATH}, {TEST_WORKERS}))")
            print(m_get.call_count)




