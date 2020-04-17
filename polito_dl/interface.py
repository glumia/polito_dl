from functools import wraps

from requests import Session

from polito_dl.auth import login
from polito_dl.scraping import course_data


class AuthenticationNeeded(Exception):
    pass


class PolitoDownloader:
    def __init__(self):
        self.session = Session()
        self.authenticated = False

    def login(self, username, password):
        login(self.session, username, password)
        self.authenticated = True

    def check_authentication(self, func):
        @wraps(func)
        def wrapper():
            if not self.authenticated:
                raise AuthenticationNeeded
            return func

        return wrapper()

    @check_authentication
    def get_course_data(self, url):
        return course_data(self.session, url)
