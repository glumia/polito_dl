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

# Example of response of GET request to "https://idp.polito.it:443/idp/profile/SAML2/Redirect/SSO"
# or POST to "https://login.didattica.polito.it/secure/ShibLogin.php", both are redirected to
# "https://idp.polito.it/idp/profile/SAML2/Redirect/SSO".
fake_sso_content = """<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        </head>
    <body onload="document.forms[0].submit()">
        <noscript>
            <p>
                <strong>Note:</strong> Since your browser does not support JavaScript,
                you must press the Continue button once to proceed.
            </p>
        </noscript>
        
        <form action="https&#x3a;&#x2f;&#x2f;www.polito.it&#x2f;Shibboleth.sso&#x2f;SAML2&#x2f;POST" method="post">
            <div>
                <input type="hidden" name="RelayState" value="cookie&#x3a;dummy_value"/>                
                                
                <input type="hidden" name="SAMLResponse" value="dummy_saml_response"/>                
            </div>
            <noscript>
                <div>
                    <input type="submit" value="Continue"/>
                </div>
            </noscript>
        </form>
            </body>
</html>"""


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
