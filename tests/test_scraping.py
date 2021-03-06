from unittest.mock import Mock, patch

import pytest
from requests import Session

from polito_dl.scraping import (
    base_url,
    course_data,
    download_paths,
    direct_download_url,
)


@pytest.mark.parametrize(
    "path",
    [
        "/portal/pls/portal/sviluppo.videolezioni.vis?cor=456",
        "/pls/portal30/sviluppo.videolezioni.vis?cor=456",
    ],
)
@patch("polito_dl.scraping.get_course_data")
@patch("polito_dl.scraping.parse_html")
def test_course_data(parse_html, get_course_data, path):
    url = base_url + path

    html_content = "dummy_content"
    session = Mock()
    dummy_response = Mock()
    dummy_response.content = html_content
    session.get.return_value = dummy_response

    soup = "dummy_soup"
    parse_html.return_value = soup

    expected_data = "dummy_data"
    get_course_data.return_value = expected_data

    data = course_data(session, url)

    session.get.assert_called_with(url)
    parse_html.assert_called_with(html_content)
    get_course_data.assert_called_with(soup)
    assert data == expected_data


def test_course_data_invalid_url():
    invalid_url = (
        "https://elearning.polito.it/courses/2011_PRE_MATE_ENG/document/"
        "Videolezioni.html?cidReq=2011_PRE_MATE_ENG"
    )
    session = Mock()

    with pytest.raises(ValueError):
        course_data(session, invalid_url)


@patch("polito_dl.scraping.get_download_paths")
@patch("polito_dl.scraping.parse_html")
def test_download_paths(parse_html, get_download_paths):
    path = "sviluppo.videolezioni.vis?cor=456&arg=Lezioni%20on-line&lez=21927"

    html_content = "dummy_content"
    session = Mock()
    dummy_response = Mock()
    dummy_response.content = html_content
    session.get.return_value = dummy_response

    soup = "dummy_soup"
    parse_html.return_value = soup

    expected_data = "dummy_data"
    get_download_paths.return_value = expected_data

    data = download_paths(session, path)

    session.get.assert_called_with(base_url + "/pls/portal30/" + path)
    parse_html.assert_called_with(html_content)
    get_download_paths.assert_called_with(soup)
    assert data == expected_data


def test_download_paths_invalid_path():
    invalid_path = "Videolezioni.html?cidReq=2011_PRE_MATE_ENG"
    session = Mock()

    with pytest.raises(ValueError):
        direct_download_url(session, invalid_path)


def test_direct_download_url(requests_mock):
    path = "/pls/portal30/sviluppo.videolezioni.download?fid=76424"
    durl = "dummy_download_url"

    requests_mock.get(base_url + path, status_code=302, headers={"Location": durl})

    assert direct_download_url(Session(), path) == durl


def test_direct_download_url_invalid_path():
    invalid_path = "/pls/portal30/sviluppo.videolezioni.vis?cor=456"
    session = Mock()

    with pytest.raises(ValueError):
        direct_download_url(session, invalid_path)
