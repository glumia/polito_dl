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
)

with open("tests/html/SSO.html", "r") as fp:
    fake_sso_content = fp.read()


def test_get_relay_state():
    assert get_relay_state(fake_sso_content) == "cookie:dummy_value"


def test_get_saml_response():
    assert get_saml_response(fake_sso_content) == "dummy_saml_response"


def test_get_relay_state_not_found():
    malformed_html = "dummy_content"
    with pytest.raises(RelayStateNotFound):
        get_relay_state(malformed_html)


def test_get_saml_response_not_found():
    malformed_html = "dummy_content"
    with pytest.raises(SAMLResponseNotFound):
        get_saml_response(malformed_html)


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
        resp = session.get(
            "https://didattica.polito.it/portal/page/portal/home/Studente"
        )
        assert resp.status_code == 200
