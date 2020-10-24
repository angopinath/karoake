from files import file_utils


class ScraperSite:

    def __init__(self, source_url: str):
        self.source_url = source_url
        self.downloadables = []

    def find_songs(self):
        pass

    def find_all_songs(self):
        pass

    def export(self, file):
        file_utils.save_list(self.downloadables, file)