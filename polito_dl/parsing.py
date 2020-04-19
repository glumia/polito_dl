from bs4 import BeautifulSoup


def parse_html(html_content):
    return BeautifulSoup(html_content, "html.parser")


def get_course_name(soup):
    tag = soup.find("div", {"class": "h2 text-primary"})
    return tag.text


def get_professor_name(soup):
    return soup.h3.text.replace("Prof.", "").strip()


def get_lecture_name(lecture_tag):
    return lecture_tag.a.text


def get_lecture_date(lecture_tag):
    return lecture_tag.span.text.replace("del\xa0", "")


def get_lecture_path(lecture_tag):
    return lecture_tag.a["href"]


def get_lecture_topics(lecture_detail_tag):
    topic_tags = lecture_detail_tag.findAll("a")
    return [tag.text for tag in topic_tags]


def get_lectures_data(soup):
    navbar_content = soup.find("ul", {"id": "navbar_left_menu"})
    lecture_tags = navbar_content.findAll("li", {"class": "h5"})
    lecture_detail_tags = navbar_content.findAll("li", {"class": "h6 argomentiEspansi"})
    return [
        {
            "name": get_lecture_name(ltag),
            "date": get_lecture_date(ltag),
            "path": get_lecture_path(ltag),
            "topics": get_lecture_topics(ldetailtag),
        }
        for ltag, ldetailtag in zip(lecture_tags, lecture_detail_tags)
    ]


def get_course_data(soup):
    course_name = get_course_name(soup)
    professor_name = get_professor_name(soup)
    lectures_data = get_lectures_data(soup)
    return {
        "name": course_name,
        "professor": professor_name,
        "lectures": lectures_data,
    }


def get_video_path(soup):
    tag = soup.find("a", text="Video")
    return tag["href"]


def get_iphone_path(soup):
    tag = soup.find("a", text="iPhone")
    return tag["href"]


def get_audio_path(soup):
    tag = soup.find("a", text="Audio")
    return tag["href"]


def get_download_paths(soup):
    return {
        "video": get_video_path(soup),
        "iphone": get_iphone_path(soup),
        "audio": get_audio_path(soup),
    }
