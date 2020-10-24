import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

proxies = {
'http': '',
'https': '',
}


def get_page(url:str):
    return requests.get(url, proxies=proxies, allow_redirects=True)


def scrap(url: str) -> BeautifulSoup:
    page = requests.get(url, proxies=proxies, allow_redirects=True)
    return BeautifulSoup(page.content, 'html.parser')


def get_host_from_url(url: str) -> str:
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

