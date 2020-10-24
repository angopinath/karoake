import sites.web_scraper as scraper
from sites.base import ScraperSite


class TamilMusix(ScraperSite):

    def __init__(self, source_url: str):
        ScraperSite.__init__(self, source_url)
        self.base_context = scraper.get_host_from_url(self.source_url)

    def find_songs(self):
        songs = TamilMusix.__get_song_pages__(self.source_url)
        download_urls = [TamilMusix.__handle_page__(self.base_context + song) for song in songs]
        self.downloadables.extend(download_urls)

    def find_all_songs(self):
        soup = scraper.scrap(self.source_url)
        page_soap = soup.find("div",{'class':'pages'})
        pages = [int(a.text.strip()) for a in page_soap.find_all('a') if a.text.strip()]
        songs = []
        songs.extend(TamilMusix.__get_song_pages__(self.source_url))
        for i in pages:
            songs.extend(TamilMusix.__get_song_pages__(self.source_url +"?page="+str(i)))
        self.downloadables.extend([TamilMusix.__handle_page__(self.base_context + song) for song in songs])

    @staticmethod
    def __get_song_pages__(url: str):
        soup = scraper.scrap(url)
        songs = soup.find_all("div", class_= 'song')
        return [song.find('a')['href'] for song in songs]

    @staticmethod
    def __handle_page__(url: str):
        soup = scraper.scrap(url)
        download_element = soup.find_all("div",{'class':'down', 'align':'left'})[-1]
        return download_element.find('a')['href']

