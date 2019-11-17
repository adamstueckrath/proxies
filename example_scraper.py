from proxies import Proxy

from urllib.parse import urlencode

import requests
from fake_useragent import UserAgent


class Scraper:

    def __init__(self, url_base, custom_headers=None):
        self.url_base = url_base
        self.custom_headers = custom_headers
        self.proxy = Proxy()
        self.user_agent = UserAgent()

    @staticmethod
    def make_url(url, *res, **params):
        for r in res:
            url = '{}/{}'.format(url, r)
        if params:
            url = '{}?{}'.format(url, urlencode(params))
        return url

    def set_proxy(self, session):
        """
        Configure the session to use one of the proxy_candidates.  If verify is
        True, then the proxy will have been verified to work.
        """
        proxy = self.proxy.get_proxy()
        while True:
            session.proxies = {
                'https': 'https://{}:{}'.format(proxy['IP Address'],
                                                proxy['Port'])
            }
            try:
                return session.get('https://httpbin.org/ip').json()
            except Exception:
                proxy = self.proxy.get_proxy()

    def crawl(self, *url_path, **url_params):
        session = requests.Session()
        if self.custom_headers:
            session.headers = self.custom_headers
        url_crawl = self.make_url(self.url_base, *url_path, **url_params)
        while True:
            try:
                session.headers = {'User-Agent': self.user_agent.random}
                self.set_proxy(session)
                response = session.get(url_crawl)
                response.raise_for_status()
                return response.text
            except (requests.exceptions.HTTPError,
                    requests.exceptions.ProxyError,
                    requests.exceptions.SSLError):
                pass
