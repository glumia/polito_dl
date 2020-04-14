import os

import pytest
from requests.sessions import Session

from polito_dl.auth import (
    get_relay_state,
    get_saml_response,
    InvalidCredentials,
    login,
    RelayStateNotFound,
    SAMLResponseNotFound,
    get_sso_params,
)
from polito_dl.utils import parse_html

with open("tests/html/SSO.html", "r") as fp:
    sso_content = fp.read()
sso_content_soup = parse_html(sso_content)


def test_get_relay_state():
    assert get_relay_state(sso_content_soup) == "cookie:dummy_value"


def test_get_saml_response():
    assert get_saml_response(sso_content_soup) == "dummy_saml_response"


def test_get_relay_state_not_found():
    malformed_html = parse_html("dummy_content")
    with pytest.raises(RelayStateNotFound):
        get_relay_state(malformed_html)


def test_get_saml_response_not_found():
    malformed_html = parse_html("dummy_content")
    with pytest.raises(SAMLResponseNotFound):
        get_saml_response(malformed_html)


def test_get_sso_params():
    relay_state, saml_response = get_sso_params(sso_content)
    assert relay_state == "cookie:dummy_value"
    assert saml_response == "dummy_saml_response"


def test_login_invalid_credentials(requests_mock):
    requests_mock.get("https://idp.polito.it/idp/x509mixed-login")
    requests_mock.post("https://idp.polito.it/idp/Authn/X509Mixed/UserPasswordLogin")
    # If login is successful the previous request should redirect to
    # "https://idp.polito.it:443/idp/profile/SAML2/Redirect/SSO", here we are
    # intentionally *not* doing this.
    with pytest.raises(InvalidCredentials):
        with Session() as session:
            login(session, "dummy_username", "dummy_password")


def test_login():
    username = os.getenv("POLITO_USERNAME")
    password = os.getenv("POLITO_PASSWORD")
    with Session() as session:
        login(session, username, password)
        resp = session.head(
            "https://didattica.polito.it/portal/page/portal/home/Studente"
        )
        assert resp.status_code == 200
