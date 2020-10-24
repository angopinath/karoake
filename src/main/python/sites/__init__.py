from sites.tamil_musix import TamilMusix
from sites.isaimini import IsaiMini


class ScraperSiteOpt:

    @staticmethod
    def __get_scraper_site__(site):

        if 'tamilmusix' in site:
            return TamilMusix(site)
        elif 'isaimini' in site:
            return IsaiMini(site)
        else:
            return TypeError('This site {} is not supported now'.format(site))
