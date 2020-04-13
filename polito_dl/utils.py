from bs4 import BeautifulSoup


def parse_html(html_content):
    return BeautifulSoup(html_content, "html.parser")
