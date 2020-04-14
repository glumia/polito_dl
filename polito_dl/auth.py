import ssl

from requests.adapters import HTTPAdapter, DEFAULT_POOLBLOCK, PoolManager

from polito_dl.utils import parse_html


class RelayStateNotFound(ValueError):
    pass


def get_relay_state(soup):
    tag = soup.find("input", {"name": "RelayState"})
    if not tag:
        raise RelayStateNotFound
    return tag["value"]


class SAMLResponseNotFound(ValueError):
    pass


def get_saml_response(soup):
    tag = soup.find("input", {"name": "SAMLResponse"})
    if not tag:
        raise SAMLResponseNotFound
    return tag["value"]


def get_sso_params(html_content):
    soup = parse_html(html_content)
    relay_state = get_relay_state(soup)
    saml_response = get_saml_response(soup)
    return relay_state, saml_response


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

    relay_state, saml_response = get_sso_params(resp.text)
    session.post(
        "https://www.polito.it/Shibboleth.sso/SAML2/POST",
        data={"RelayState": relay_state, "SAMLResponse": saml_response},
    )

    session.mount("https://login.didattica.polito.it", LegacyHTTPSAdapter())
    resp = session.post("https://login.didattica.polito.it/secure/ShibLogin.php")

    relay_state, saml_response = get_sso_params(resp.text)
    session.post(
        "https://login.didattica.polito.it/Shibboleth.sso/SAML2/POST",
        data={"RelayState": relay_state, "SAMLResponse": saml_response},
    )

    resp = session.head("https://didattica.polito.it/portal/page/portal/home/Studente")
    assert resp.status_code == 200
