import json
import os
from getpass import getpass
from math import ceil

import click
import requests

from polito_dl import PolitoDownloader

DEFAULT_CHUNK_SIZE = 1000 * 1000  # 1 MB


def get_authenticated_client(ctx):
    username = ctx.obj["username"]
    password = ctx.obj["password"]
    if not username:
        username = click.prompt("Username")
    if not password:
        password = getpass("Password: ")
    pdl = PolitoDownloader()
    pdl.login(username, password)
    return pdl


def retrieve(url, chunk_size=DEFAULT_CHUNK_SIZE):
    resp = requests.head(url, stream=True)
    file_size = int(resp.headers["Content-Length"])
    filename = resp.url.split("/")[-1]
    first_byte = os.path.getsize(filename) if os.path.exists(filename) else 0
    if first_byte >= file_size:
        return file_size
    resp = requests.get(
        url, headers={"Range": "bytes=%s-%s" % (first_byte, file_size)}, stream=True
    )
    with open(filename, "ab") as fp:
        with click.progressbar(
            iterable=resp.iter_content(chunk_size=chunk_size),
            length=ceil(file_size / chunk_size),
            label=filename,
            show_eta=True,
        ) as pbar:
            for chunk in pbar:
                fp.write(chunk)
    return file_size


@click.group()
@click.option("--username", type=str, help="Do not prompt for username.")
@click.option(
    "--password",
    default=None,
    type=str,
    help="Do not prompt for password. (Warning: this could be insecure, use it only if "
    "you know what you are doing.)",
)
@click.pass_context
def main(ctx, username, password):
    ctx.obj = {"username": username, "password": password}


@main.command()
@click.argument("url", nargs=1)
@click.pass_context
def print_course_json(ctx, url):
    """Print course information in JSON format."""
    pdl = get_authenticated_client(ctx)
    click.echo(json.dumps(pdl.get_course_data(url), indent=4))


@main.command()
@click.option("--all", is_flag=True, help="Download all course's lectures.")
@click.option(
    "--format",
    default="video",
    type=click.Choice(["video", "iphone", "audio"], case_sensitive=False),
    help="Select media format to download (default: video).",
)
@click.option(
    "--chunk-size",
    default=DEFAULT_CHUNK_SIZE,
    type=int,
    help="Set downloader chunk size (default: 1MB).",
)
@click.argument("url", nargs=1)
@click.pass_context
def download(ctx, url, all, format, chunk_size):
    """Download lecture(s)."""
    pdl = get_authenticated_client(ctx)
    if all:
        course = pdl.get_course_data(url)
        paths = (lecture["path"] for lecture in course["lectures"])
    else:
        paths = (url.split("/")[-1],)

    for path in paths:
        dl_url = pdl.get_download_url(path, format)
        retrieve(dl_url, chunk_size)
