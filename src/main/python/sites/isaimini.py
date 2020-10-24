import sites.web_scraper as scraper
from sites.base import ScraperSite


class IsaiMini(ScraperSite):

    def __init__(self, source_url: str):
        ScraperSite.__init__(self, source_url)
        self.base_context = scraper.get_host_from_url(self.source_url)

    def find_songs(self):
        songs = IsaiMini.__get_song_pages__(self.source_url)
        download_urls = [IsaiMini.__handle_page__(song) for song in songs]
        self.downloadables.extend(download_urls)

    def find_all_songs(self):
        soup = scraper.scrap(self.source_url)
        page_soap = soup.find("div",{'class':'isaiminida'})
        pages = [a['href'].strip() for a in page_soap.find_all('a') if a.text.strip()]
        songs = []
        songs.extend(IsaiMini.__get_song_pages__(self.source_url))
        for i in pages:
            songs.extend(IsaiMini.__get_song_pages__(i))
        self.downloadables.extend([IsaiMini.__handle_page__(song) for song in songs])

    @staticmethod
    def __get_song_pages__(url: str):
        soup = scraper.scrap(url)
        songs = soup.find_all("div", class_= 'f')
        return [song.find('a')['href'] for song in songs]

    @staticmethod
    def __handle_page__(url: str):
        soup = scraper.scrap(url)
        div = soup.find_all('div', {'class': 'bf'})[0]
        download_element = div.find_all("a",{'rel': 'nofollow'})[-1]
        return download_element['href']

