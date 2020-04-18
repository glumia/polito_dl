import json
from getpass import getpass

import click

from polito_dl import PolitoDownloader
from polito_dl.auth import InvalidCredentials


@click.command("polito_dl")
@click.option("--username", type=str)
@click.option("--password", type=str)
@click.option(
    "--print-course", is_flag=True, help="Print JSON of course data and exit."
)
@click.option(
    "--format",
    default="video",
    type=click.Choice(["video", "iphone", "audio"], case_sensitive=False),
    help="Specify download's url content format. Default: video.",
)
@click.argument("url")
def main(username, password, print_course, format, url):
    """Get lecture direct download URL or print info on course."""
    pdl = PolitoDownloader()
    if not username:
        username = input("Username: ")
    if not password:
        password = getpass("Password: ")

    try:
        pdl.login(username, password)
    except InvalidCredentials:
        click.echo("Login failed, check your username and password.")
        return

    if print_course:
        click.echo(json.dumps(pdl.get_course_data(url), indent=4))
        return

    path = url.split("/")[-1]
    click.echo(pdl.get_download_url(path, format=format))
