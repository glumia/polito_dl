from requests import Session

from polito_dl.auth import login
from polito_dl.scraping import course_data, download_paths, direct_download_url


class AuthenticationNeeded(Exception):
    pass


class PolitoDownloader:
    def __init__(self):
        self._session = Session()
        self._authenticated = False

    def login(self, username, password):
        login(self._session, username, password)
        self._authenticated = True

    @property
    def authenticated(self):
        return self._authenticated

    def _check_authentication(self):
        if not self._authenticated:
            raise AuthenticationNeeded

    def get_course_data(self, url):
        self._check_authentication()
        return course_data(self._session, url)

    def get_download_url(self, path, format="video"):
        self._check_authentication()

        if format not in {"video", "audio", "iphone"}:
            raise ValueError("invalid download format")

        dl_path = download_paths(self._session, path)[format]
        return direct_download_url(self._session, dl_path)
