import requests
from bs4 import BeautifulSoup


class Proxy:
    PROXIES_URL = 'https://www.sslproxies.org/'

    def __init__(self):
        self.proxies = []

    @property
    def proxies_size(self):
        return len(self.proxies)

    def _get_proxies(self):
        try:
            response = requests.get(self.PROXIES_URL)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        proxy_table = soup.find('table', id='proxylisttable')
        headers = [th.get_text()
                   for th in proxy_table.find('tr').find_all('th')
                   ]

        for row in proxy_table.find_all('tr')[1:]:
            result = zip(headers,
                         (td.get_text() for td in row.find_all('td'))
                         )
            self.proxies.append(dict(result))

    def get_proxy(self):
        '''Returns a proxy when called.
        Returns an empty dict when fails.
        '''
        # could call check_proxy to validate it here, and break that logic into
        # another private function, or just make the check a static method and
        # force user to validate if wanted...

        # collect a working proxy to be used to fetch a valid response
        # as soon as it fetches a valid response,
        # it will break out of the while loop

        if self.proxies:
            return self.proxies.pop(0)
        else:
            try:
                self._get_proxies()
            except Exception:
                pass

        if self.proxies:
            return self.proxies.pop(0)

        return {}


if __name__ == '__main__':
    import pprint
    p = Proxy()
    x = p.get_proxy()
    print(x)
    print(p.proxies_size)
