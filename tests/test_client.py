from unittest.mock import patch

import pytest

from polito_dl.client import PolitoDownloader, AuthenticationNeeded


@pytest.fixture
def pdl():
    return PolitoDownloader()


def test_init(pdl):
    assert pdl.authenticated is False


@patch("polito_dl.client.login")
def test_login(login, pdl):
    username = "dummy_username"
    password = "dummy_password"

    pdl.login(username, password)

    login.assert_called_with(pdl._session, username, password)
    assert pdl.authenticated is True


def test_authentication_not_settable(pdl):
    with pytest.raises(AttributeError):
        pdl.authenticated = True


def test_check_authentication(pdl):
    with pytest.raises(AuthenticationNeeded):
        pdl._check_authentication()

    pdl._authenticated = True
    pdl._check_authentication()


@patch("polito_dl.client.course_data")
def test_get_course_data(course_data, pdl):
    url = "dummy_url"
    course_data.return_value = expected = "dummy_data"

    pdl._authenticated = True
    data = pdl.get_course_data(url)

    course_data.assert_called_with(pdl._session, url)
    assert data == expected


def test_get_course_data_auth_error(pdl):
    with pytest.raises(AuthenticationNeeded):
        pdl.get_course_data("dummy_url")


@pytest.mark.parametrize("format", ["video", "audio", "iphone"])
@patch("polito_dl.client.direct_download_url")
@patch("polito_dl.client.download_paths")
def test_get_download_url(download_paths, direct_download_url, format, pdl):
    path = "dummy_lecture_path"

    video_path = "dummy_video_path"
    audio_path = "dummy_audio_path"
    iphone_path = "dummy_iphone_path"
    download_paths.return_value = dl_paths = {
        "video": video_path,
        "audio": audio_path,
        "iphone": iphone_path,
    }

    direct_download_url.return_value = expected = "dummy_dl_url"

    pdl._authenticated = True
    dl_url = pdl.get_download_url(path, format)

    download_paths.assert_called_with(pdl._session, path)
    direct_download_url.assert_called_with(pdl._session, dl_paths[format])
    assert dl_url == expected


def test_get_download_url_invalid_format(pdl):
    pdl._authenticated = True

    with pytest.raises(ValueError):
        pdl.get_download_url("dummy_path", "invalid_format")


def test_get_download_url_auth_error(pdl):
    with pytest.raises(AuthenticationNeeded):
        pdl.get_download_url("dummy_path", "video")
