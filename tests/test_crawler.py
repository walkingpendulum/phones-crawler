from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

import crawler


class TestCrawler(AioHTTPTestCase):
    async def get_application(self):
        async def handler(request):
            return web.Response(text=request.match_info['id'])

        app = web.Application()
        app.router.add_get('/{id}', handler)
        return app

    def test_crawl_echo_server(self):
        urls = [f'http://{self.client.host}:{self.client.port}/{id_}' for id_ in range(10)]
        results = crawler.run(urls=urls, limit=5, loop=self.loop)

        self.assertSetEqual(set(results), set(map(str, range(10))))
