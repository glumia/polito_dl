from getpass import getpass

import click

from polito_dl import PolitoDownloader
from polito_dl.auth import InvalidCredentials


@click.command("polito_dl")
@click.option("--username", type=str)
@click.option("--password", type=str)
@click.option("--course-data", default=False, help="Print course data and exit.")
@click.option(
    "--format",
    default="video",
    type=click.Choice(["video", "iphone", "audio"], case_sensitive=False),
    help="",
)
@click.argument("url")
def cli(username, password, course_data, format, url):
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

    if course_data:
        pass


if __name__ == "__main__":
    cli()
