import re
import html
import ssl

from requests.adapters import HTTPAdapter, DEFAULT_POOLBLOCK, PoolManager


class RelayStateNotFound(ValueError):
    pass


def get_relay_state(html_content):
    pattern = r'.*name="RelayState" value="(.*)".*'
    match = re.search(pattern, html_content)
    if not match:
        raise RelayStateNotFound
    relay_state = html.unescape(match.groups()[0])
    return relay_state


class SAMLResponseNotFound(ValueError):
    pass


def get_saml_response(html_content):
    pattern = r'.*name="SAMLResponse" value="(.*)".*'
    match = re.search(pattern, html_content)
    if not match:
        raise SAMLResponseNotFound
    saml_response = match.groups()[0]
    return saml_response


class InvalidCredentials(ValueError):
    pass


class LegacyHTTPSAdapter(HTTPAdapter):
    def init_poolmanager(
        self, connections, maxsize, block=DEFAULT_POOLBLOCK, **pool_kwargs
    ):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1,
        )


def login(session, username, password):
    session.get("https://idp.polito.it/idp/x509mixed-login")
    resp = session.post(
        "https://idp.polito.it/idp/Authn/X509Mixed/UserPasswordLogin",
        data={"j_username": username, "j_password": password},
    )

    if resp.url != "https://idp.polito.it:443/idp/profile/SAML2/Redirect/SSO":
        raise InvalidCredentials("check username and password.")

    relaystate = get_relay_state(resp.text)
    samlresponse = get_saml_response(resp.text)
    session.post(
        "https://www.polito.it/Shibboleth.sso/SAML2/POST",
        data={"RelayState": relaystate, "SAMLResponse": samlresponse},
    )

    session.mount("https://login.didattica.polito.it", LegacyHTTPSAdapter())
    resp = session.post("https://login.didattica.polito.it/secure/ShibLogin.php")
    relaystate = get_relay_state(resp.text)
    samlresponse = get_saml_response(resp.text)
    session.post(
        "https://login.didattica.polito.it/Shibboleth.sso/SAML2/POST",
        data={"RelayState": relaystate, "SAMLResponse": samlresponse},
    )

    resp = session.head("https://didattica.polito.it/portal/page/portal/home/Studente")
    assert resp.status_code == 200
