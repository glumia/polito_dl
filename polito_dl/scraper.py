import html
import re


def get_videolesson_paths(html_content):
    pattern = r'<a.*href="(sviluppo.videolezioni.vis.*)">.*'
    matches = re.findall(pattern, html_content)
    paths = (
        path for path in matches if "seek" not in path
    )  # Filter out links to specific arguments of videolessons
    unescaped_paths = [html.unescape(path) for path in paths]
    return unescaped_paths
