from bs4 import BeautifulSoup

from polito_dl.parsing import (
    parse_html,
    get_course_name,
    get_professor_name,
    get_lecture_name,
    get_lecture_date,
    get_lecture_path,
    get_lecture_topics,
    get_lectures_data,
    get_course_data,
    get_video_path,
    get_iphone_path,
    get_audio_path,
    get_download_paths,
)


def test_parse_html():
    assert isinstance(parse_html("dummy_html_content"), BeautifulSoup)


with open("tests/fixtures/sviluppo_videolezioni_vis.html", "r") as fp:
    course_page_content = fp.read()
course_soup = BeautifulSoup(course_page_content, features="html.parser")
lecture_tag = course_soup.find("ul", {"id": "navbar_left_menu"}).find(
    "li", {"class": "h5"}
)
lecture_details_tag = course_soup.find("ul", {"id": "navbar_left_menu"}).find(
    "li", {"class": "h6 argomentiEspansi"}
)


def test_get_course_name():
    course_name = get_course_name(course_soup)
    assert course_name == "Algoritmi e programmazione"


def test_get_professor_name():
    professor_name = get_professor_name(course_soup)
    assert professor_name == "Paolo Enrico CAMURATI"


def test_get_lecture_name():
    lecture_name = get_lecture_name(lecture_tag)
    assert lecture_name == "2020_Lezione 01"


def test_get_lecture_date():
    lecture_date = get_lecture_date(lecture_tag)
    assert lecture_date == "30/09/2019"


def test_get_lecture_path():
    lecture_path = get_lecture_path(lecture_tag)
    assert (
        lecture_path
        == "sviluppo.videolezioni.vis?cor=456&arg=Lezioni%20on-line&lez=19638"
    )


def test_get_lecture_topics():
    lecture_topics = get_lecture_topics(lecture_details_tag)
    assert set(lecture_topics) == {"Introduzione al corso"}


def test_get_lectures_data():
    lectures_data = get_lectures_data(course_soup)
    expected_lectures_data = [
        {
            "name": "2020_Lezione 01",
            "date": "30/09/2019",
            "path": "sviluppo.videolezioni.vis?cor=456&arg=Lezioni%20on-line&lez=19638",
            "topics": ["Introduzione al corso"],
        },
        {
            "name": "2020_Lezione 02",
            "date": "30/09/2019",
            "path": "sviluppo.videolezioni.vis?cor=456&arg=Lezioni%20on-line&lez=19649",
            "topics": ["L'essenziale del linguaggio C (parte 1)"],
        },
        {
            "name": "2020_Lezione 03",
            "date": "01/10/2019",
            "path": "sviluppo.videolezioni.vis?cor=456&arg=Lezioni%20on-line&lez=19668",
            "topics": ["Gli Algoritmi"],
        },
        {
            "name": "2020_Lezione 04",
            "date": "03/10/2019",
            "path": "sviluppo.videolezioni.vis?cor=456&arg=Lezioni%20on-line&lez=19818",
            "topics": ["L'essenziale del linguaggio C (parte 2)"],
        },
        {
            "name": "2020_Lezione 05",
            "date": "03/10/2019",
            "path": "sviluppo.videolezioni.vis?cor=456&arg=Lezioni%20on-line&lez=19726",
            "topics": ["Esercitazione 01 - Gomoku"],
        },
        {
            "name": "2020_Lezione 06",
            "date": "07/10/2019",
            "path": "sviluppo.videolezioni.vis?cor=456&arg=Lezioni%20on-line&lez=20920",
            "topics": ["Gli Algoritmi", "Analisi della complessita'"],
        },
    ]
    assert all(
        all(
            (
                lect["name"] == exp_lect["name"],
                lect["date"] == exp_lect["date"],
                lect["path"] == exp_lect["path"],
                set(lect["topics"]) == set(exp_lect["topics"]),
            )
        )
        for lect, exp_lect in zip(lectures_data, expected_lectures_data)
    )


def test_get_course_data():
    assert get_course_data(course_soup) == {
        "name": get_course_name(course_soup),
        "professor": get_professor_name(course_soup),
        "lectures": get_lectures_data(course_soup),
    }


def test_get_video_path():
    assert (
        get_video_path(course_soup)
        == "/pls/portal30/sviluppo.videolezioni.download?fid=76422"
    )


def test_get_iphone_path():
    assert (
        get_iphone_path(course_soup)
        == "/pls/portal30/sviluppo.videolezioni.download?fid=76424"
    )


def test_get_audio_path():
    assert (
        get_audio_path(course_soup)
        == "/pls/portal30/sviluppo.videolezioni.download?fid=76423"
    )


def test_get_download_paths():
    assert get_download_paths(course_soup) == {
        "video": get_video_path(course_soup),
        "iphone": get_iphone_path(course_soup),
        "audio": get_audio_path(course_soup),
    }
