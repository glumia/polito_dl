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


def get_course_name(html_content):
    pattern = r'.*class="h2 text-primary">(.*)<'
    match = re.search(pattern, html_content)
    return match.groups()[0] if match else None


def get_professor_name(html_content):
    pattern = r".*Prof\.\s*(.*)<"
    match = re.search(pattern, html_content)
    return match.groups()[0] if match else None


# TODO: Use BeautifulSoup for lectures info scraping, regex is really not viable for
#       this.

# def get_navbar_content(html_content):
#     start = html_content.find('<ul id="navbar_left_menu">')
#     if start == -1:
#         return None
#     end = html_content.find("</ul>", start)
#     return html_content[start:end]
#
#
# def get_lecture_topics(navbar_content, lecture_id):
#     pattern = f"lez={lecture_id}.*seek.*>(.*)<"
#     lecture_topics = re.findall(pattern, navbar_content)
#     return lecture_topics or None
#
#
# def get_lectures_info(html_content):
#     navbar_content = get_navbar_content(html_content)
#     if not navbar_content:
#         return None
#     pattern = r'.*videolezioni.vis.*lez=([^&"]*).*>(.*)<.*\n.*(\d{2}/\d{2}/\d{4})'
#     matches = re.findall(pattern, navbar_content)
#     lectures_info = [
#         {
#             "name": match[1],
#             "date": match[2],
#             "topics": get_lecture_topics(navbar_content, match[0]),
#         }
#         for match in matches
#     ]
#     return lectures_info
#
#
# def get_syllabus(html_content):
#     syllabus = dict()
#     syllabus["course_name"] = get_course_name(html_content)
#     syllabus["professor_name"] = get_professor_name(html_content)
#     syllabus["lectures"] = get_lectures_info(html_content)
#     return syllabus
