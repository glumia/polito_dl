from requests import Session

from polito_dl.auth import login
from polito_dl.scraping import course_data, lecture_download_paths, direct_download_url
from polito_dl.utilities import download_file


class AuthenticationNeeded(Exception):
    pass


class PolitoDownloader:
    def __init__(self):
        self.session = Session()
        self.authenticated = False

    def login(self, username, password):
        login(self.session, username, password)
        self.authenticated = True

    def _check_authentication(self):
        if not self.authenticated:
            raise AuthenticationNeeded

    def get_course_data(self, url):
        self._check_authentication()
        return course_data(self.session, url)

    def get_download_url(self, url, format="video"):
        self._check_authentication()

        if format not in {"video", "audio", "iphone"}:
            raise ValueError("invalid download format")

        path = lecture_download_paths(self.session, url)[format]
        return direct_download_url(self.session, path)

    def download(
        self, url, format="video", filename=None, chunk_size=None, quiet=False
    ):
        self._check_authentication()

        if format not in {"video", "audio", "iphone"}:
            raise ValueError("invalid download format")

        dl_url = self.get_download_url(url, format)
        download_file(dl_url, filename, chunk_size, quiet)
