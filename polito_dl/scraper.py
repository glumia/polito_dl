from polito_dl.utils import parse_html


def get_videolesson_paths(html_content):
    soup = parse_html(html_content)
    navbar_content = soup.find("ul", {"id": "navbar_left_menu"})
    tags = navbar_content.findAll("li", {"class": "h5"})
    paths = [tag.a["href"] for tag in tags]
    return paths


def get_course_name(html_content):
    soup = parse_html(html_content)
    tag = soup.find("div", {"class": "h2 text-primary"})
    return tag.text


def get_professor_name(html_content):
    soup = parse_html(html_content)
    return soup.h3.text.replace("Prof.", "").strip()


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
