#!/usr/bin/python3
"""Usage:
    polito_dl [options] URL

Options:
    -a, --auth-file FILE       Get login credentials from FILE
    --list-lectures            List lectures available for download and exit
    --print-syllabus           Print the course syllabus and exit
    --save-syllabus FILE       Save the course syllabus into file and exit
    --lecture-start NUMBER     Lecture to start download at (default is 1)
    --lecture-end NUMBER       Lecture to end download at (default is last)
    --lecture-items ITEM_SPEC  Lectures to download. Specify indices of
                               the lectures separated by commas like:
                               "--lecture-items 1,2,5,8" if you want to
                               download lectures indexed 1, 2, 5, 8 in the
                               lectures list.
    --format FORMAT            Select the download format: video,
                               iphone, audio [default: video]
    --chunk-size CSIZE         Set the downloader chunk size in
                               bytes (default 1MB)
    -q, --quiet                Activate quiet mode
    -h, --help                 Print this help and exit
    -v, --version              Print version and exit
"""

import os
import sys
import getpass
import re
import requests
import html
from docopt import docopt
from tqdm import tqdm
import json

__author__ = "gius-italy"
__license__ = "GPLv3"
__version__ = "1.1"
__email__ = "gius-italy@live.it"


def new_domain_message():
    print(
        "Please, if you found videolessons on a domain different than "
        "didattica.polito.it or elearning.polito.it send me an mail or open "
        "an issue on Github."
        )


def get_login_cookie(user, passw):
    if user is None:
        user = input("Username: ")
    if passw is None:
        passw = getpass.getpass("Password: ")
    with requests.session() as s:
        r = s.get('https://idp.polito.it/idp/x509mixed-login')
        r = s.post(
            'https://idp.polito.it/idp/Authn/X509Mixed/UserPasswordLogin',
            data={'j_username': user, 'j_password': passw})
        if r.url == "https://idp.polito.it:443/idp/profile/SAML2/Redirect/SSO":
            # Login successfull, we just need to follow some redirects
            relaystate = html.unescape(
                re.findall('name="RelayState".*value="(.*)"', r.text)[0])
            samlresponse = html.unescape(
                re.findall('name="SAMLResponse".*value="(.*)"', r.text)[0])
            r = s.post(
                'https://www.polito.it/Shibboleth.sso/SAML2/POST',
                data={'RelayState': relaystate, 'SAMLResponse': samlresponse})
            r = s.post('https://login.didattica.polito.it/secure/ShibLogin.php')
            relaystate = html.unescape(
                re.findall('name="RelayState".*value="(.*)"', r.text)[0])
            samlresponse = html.unescape(
                re.findall('name="SAMLResponse".*value="(.*)"', r.text)[0])
            r = s.post(
                'https://login.didattica.polito.it/Shibboleth.sso/SAML2/POST',
                data={'RelayState': relaystate, 'SAMLResponse': samlresponse}
                )
            login_cookie = s.cookies
        else:
            login_cookie = ""
    return login_cookie


def get_lectures_urllist(url, login_cookie):
    with requests.session() as s:
        s.cookies = login_cookie
        r = s.get(url)
    # Different html structure for videolessons on elearning.polito.it and
    # didattica.polito.it
    if "didattica.polito.it" in url:
        lectures_urllist = re.findall(
            'href="(sviluppo\.videolezioni\.vis.*lez=\w*)">', r.text)
        for i in range(len(lectures_urllist)):
            lectures_urllist[i] = \
                'https://didattica.polito.it/pls/portal30/'+html.unescape(
                lectures_urllist[i])
    elif "elearning.polito.it" in url:
        lectures_urllist = re.findall(
            "href='(template_video\.php\?[^']*)", r.text)
        for i in range(len(lectures_urllist)):
            lectures_urllist[i] = \
                'https://elearning.polito.it/gadgets/video/'+html.unescape(
                lectures_urllist[i])
    else:
        # Still under developement
        new_domain_message()
        exit(1)
        lectures_urllist = ""
    return lectures_urllist


def get_dlurl(lecture_url, login_cookie, dl_format='video'):
    with requests.session() as s:
        s.cookies = login_cookie
        r = s.get(lecture_url)
        if "didattica.polito.it" in lecture_url:
            if dl_format == 'video':
                dlurl = re.findall('href="(.*)".*Video', r.text)[0]
            if dl_format == 'iphone':
                dlurl = re.findall('href="(.*)".*iPhone', r.text)[0]
            if dl_format == 'audio':
                dlurl = re.findall('href="(.*)".*Audio', r.text)[0]
            r = s.get(
                'https://didattica.polito.it'+html.unescape(dlurl),
                allow_redirects=False)
            dlurl = r.headers['location']
        elif "elearning.polito.it" in lecture_url:
            if dl_format == 'video':
                dlurl = re.findall(
                    'href="(download.php[^\"]*).*video1', r.text)[0]
            if dl_format == 'iphone':
                dlurl = re.findall(
                    'href="(download.php[^\"]*).*video2', r.text)[0]
            if dl_format == 'audio':
                dlurl = re.findall(
                    'href="(download.php[^\"]*).*video3', r.text)[0]
            r = s.get(
                'https://elearning.polito.it/gadgets/video/' +
                html.unescape(dlurl), allow_redirects=False)
            dlurl = r.headers['location']
        else:
            # Still under developement
            new_domain_message()
            exit(1)
            dlurl = ""
    return dlurl


def download_file(dlurl, filename=None, csize=1000*1000, quiet=False):
    r = requests.get(dlurl, stream=True)
    file_size = int(r.headers['Content-Length'])
    if filename is None:
        filename = r.url.split("/")[-1]
    if os.path.exists(filename):
        first_byte = os.path.getsize(filename)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    r = requests.get(
        dlurl,
        headers={"Range": "bytes=%s-%s" % (first_byte, file_size)},
        stream=True)
    if quiet is False:
        with tqdm(total=file_size, initial=first_byte, unit='B',
                  unit_scale=True,
                  desc=filename[0:6]+"..."+filename[-7:]) as pbar:
            with open(filename, 'ab') as fp:
                for chunk in r.iter_content(chunk_size=csize):
                    fp.write(chunk)
                    pbar.update(csize)
    else:
        with open(filename, 'ab') as fp:
            for chunk in r.iter_content(chunk_size=csize):
                    fp.write(chunk)

    return file_size


def get_courses_list(login_cookie, MAX_COR = 500):
# Cerca tutte le videolezioni disponibili sulla piattaforma didattica.polito.it
# e le salva in una lista.
#
# Ad oggi 07/03/19 l'ultimo corso si trova al numero 404
#
# courses_list[i][0] Nome corso
# courses_list[i][1] Professore
# courses_list[i][2] Data della prima lezione
# courses_list[i][3] Url
    baseurl = "https://didattica.polito.it/portal/pls/portal/sviluppo.videolezioni.vis?cor="
    courses_list = []
    with requests.session() as s:
        s.cookies = lcook
        for i in range(1, MAX_COR):
            r = s.get(baseurl + str(i))
            match = re.search(
                '<div class="h2 text-primary">(.*)</div>', r.text)
            if match is not None:
                prof = re.search('<h3>\s*Prof\.\s*(.*)</h3>', r.text)
                if prof is not None:
                    prof = prof.group(1)
                date = re.search('\d{2}/(\d{2}/\d{4})', r.text)
                if date is not None:
                    date = data.group(1)
                courses_list.append([match.group(1),prof,date,r.url])
    return courses_list


def get_syllabus(url, login_cookie):
    with requests.session() as s:
        s.cookies = login_cookie
        r = s.get(url)
    syllabus = []
    if "didattica.polito.it" in url:
        course = re.search(
            '<div class="h2 text-primary">([^<]*)',
            r.text
            ).group(1)
        prof = re.search('<h3>([^<]*)', r.text).group(1)
        syllabus.append([course, prof])
        for chunk in r.text.split('<li class="h5">')[1:]:
            title = re.search(
                'href="sviluppo\.videolezioni\.vis.*lez=\w*">([^<]*)</a>',
                chunk
                ).group(1)
            date = re.search(
                '<span class="small">[^0-9]*([^<]*)',
                chunk
                ).group(1)
            arguments = re.findall('argoLink[^>]*>([^<]*)<', chunk)
            syllabus.append([title, date, arguments])
    elif "elearning.polito.it" in url:
        course = re.search(
                "<h2>(.*)</h2>",
                r.text
                ).group(1)
        prof = re.search(
                "<h3>(.*)</h3>",
                r.text
                ).group(1)
        syllabus.append([course, prof])
        # Cutting out unnecessary html
        r = r.text.split("<ul class='lezioni'")[1]
        r = r.split("</ul>")[0]
        for chunk in r.split("<li>")[1:]:
            title = re.search(
                "<a href=.*'>(.*)</a>",
                chunk
                ).group(1)
            date = re.search(
                "del&nbsp;(.*)</span>",
                chunk
                ).group(1)
            arguments = re.findall('argoLink[^>]*>([^<]*)<', chunk)
            syllabus.append([title, date, arguments])
    else:
        print("Sorry, this works only on didattica.polito.it")
        syllabus = ""
        exit(1)
    return syllabus


def print_syllabus(syllabus):
    print('\nCourse: '+syllabus[0][0])
    print('Professor: '+syllabus[0][1]+'\n')
    syllabus = syllabus[1:]
    print('Lectures')
    for i in range(len(syllabus)):
        print(syllabus[i][0]+' - '+syllabus[i][1])
        for topic in syllabus[i][2]:
            print('    '+topic)
        print('\n')


def write_syllabus(syllabus, filename=None):
    if filename is None:
        filename = 'syllabus.txt'
    with open(filename, "w") as fp:
        fp.write('Course: '+syllabus[0][0]+"\n"+"Professor: " +
                 syllabus[0][1]+"\n\n")
        for lecture in syllabus[1:]:
            fp.write(lecture[0]+" - "+lecture[1]+"\n")
            for argument in lecture[2]:
                fp.write("    "+argument+"\n")
            fp.write("\n")


def load_default_config():
    user = ''
    passw = ''
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        home = os.path.expanduser('~')
        if os.path.isfile(home+'/.config/polito_dl/auth'):
            if os.stat(home+'/.config/polito_dl/auth')[0] != 33152:
                print("\n\nWARNING!"
                      "\nAuth file permissions are not properly set."
                      "\n(Run 'chmod 600 ~/.config/polito_dl/auth')\n")
            with open(home+'/.config/polito_dl/auth', 'r') as fp:
                user, passw = json.load(fp)
    elif sys.platform.startswith('win'):
        appdata = os.getenv('APPDATA')
        if os.path.isfile(appdata+'\\polito_dl\\auth'):
            with open(appdata+'\\polito_dl\\auth', 'r') as fp:
                user, passw = json.load(fp)
    return [user, passw]


def query_yes(message):
    inp = input(message+" [Y/n] ")
    if inp[0].lower() == 'y':
        return True
    else:
        return False


def update_default_config(user, passw):
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        home = os.path.expanduser('~')
        #Update existing default config
        if os.path.isfile(home+'/.config/polito_dl/auth'):
            with open(home+'/.config/polito_dl/auth', 'r') as fp:
                strd_user, strd_passw = json.load(fp)
            if strd_user != user:
                if query_yes("\nDo you want to replace your credentials "
                             "stored in ~/.config/polito_dl/auth ?"):
                    with open(home+'/.config/polito_dl/auth', 'w') as fp:
                        json.dump([user, passw], fp)
                    os.chmod(home+'/.config/polito_dl/auth', 0o600)
            else:
                # Just update the password if needed or do nothing
                if strd_passw != passw:
                    with open(home+'/.config/polito_dl/auth', 'w') as fp:
                        json.dump([user, passw], fp)
                    os.chmod(home+'/.config/polito_dl/auth', 0o600)
        #Create a new default config
        else:
            if query_yes("\nDo you want to store your credentials in "
                         "~/.config/polito_dl/auth ?"):
                if not os.path.exists(home+'/.config/polito_dl'):
                    os.mkdir(home+'/.config/polito_dl')
                with open(home+'/.config/polito_dl/auth', 'w') as fp:
                    json.dump([user, passw], fp)
                os.chmod(home+'/.config/polito_dl/auth', 0o600)
    elif sys.platform.startswith('win'):
        appdata = os.getenv('APPDATA')
        if os.path.isfile(appdata+'\\polito_dl\\auth'):
            with open(appdata+'\\polito_dl\\auth', 'r') as fp:
                strd_user, strd_passw = json.load(fp)
            if strd_user != user:
                if query_yes("\nDo you want to replace your credentials "
                             "stored in %APPDATA%\\polito_dl\\auth ?"):
                    with open(appdata+'\\polito_dl\\auth', 'w') as fp:
                        json.dump([user, passw], fp)
            else:
                if strd_passw != passw:
                    with open(appdata+'\\polito_dl\\auth', 'w') as fp:
                        json.dump([user, passw], fp)
        else:
            if query_yes("\nDo you want to store your credentials in "
                         "%APPDATA%\\polito_dl\\auth ?"):
                if not os.path.exists(appdata+'\\polito_dl'):
                    os.mkdir(appdata+'\\polito_dl')
                with open(appdata+'\\polito_dl\\auth', 'w') as fp:
                    json.dump([user, passw], fp)


# Main
if __name__ == "__main__":
    args = docopt(__doc__, version="polito_dl "+__version__)
    if args['--auth-file'] is None:
        user, passw = load_default_config()
        if user == '':
            user = input("\nInsert your didattica.polito.it username: ")
            passw = getpass.getpass(
                    "Insert your didattica.polito.it password: ")
    else:
        with open(args['--auth-file'], 'r') as fp:
            user, passw = json.load(fp)
    if args['--lecture-start'] is None:
        start_index = 0
    else:
        start_index = int(args['--lecture-start'])-1
    if args['--lecture-end'] is None:
        end_index = 0
    else:
        end_index = int(args['--lecture-end'])-1
    if args['--lecture-items'] is not None:
        items = [int(el)-1 for el in args['--lecture-items'].split(',')]
    else:
        items = []
    if args['--format'] in ['video', 'iphone', 'audio']:
        dl_format = args['--format']
    else:
        dl_format = 'video'
    if args['--chunk-size'] is None:
        CSIZE = 1000*1000
    else:
        CSIZE = int(args['--chunk-size'])

    login_cookie = get_login_cookie(user, passw)
    while not login_cookie:
        print("\nSomething went wrong with the login, verify username and password")
        user = input("Insert your didattica.polito.it username: ")
        passw = getpass.getpass(
                "Insert your didattica.polito.it password: ")
        login_cookie = get_login_cookie(user,passw)
    update_default_config(user, passw)
    if args['--list-lectures'] is True:
        syllabus = get_syllabus(args['URL'], login_cookie)
        syllabus = syllabus[1:]
        print('\nLectures list')
        for i in range(len(syllabus)):
            print(str(i+1)+') '+syllabus[i][0])
    elif args['--print-syllabus'] is True:
        syllabus = get_syllabus(args['URL'], login_cookie)
        print_syllabus(syllabus)
    elif args['--save-syllabus'] is not None:
        syllabus = get_syllabus(args['URL'], login_cookie)
        write_syllabus(syllabus, args['--save-syllabus'])
    else:
        #Default, download all videolectures
        lect_urllist = get_lectures_urllist(args['URL'], login_cookie)
        if items:
            if not args['--quiet']:
                print("Starting download of "+str(len(items))+" lectures")
            for i in items:
                dlurl = get_dlurl(lect_urllist[i], login_cookie, dl_format)
                download_file(dlurl, csize=CSIZE, quiet=args['--quiet'])
        else:
            if end_index == 0:
                end_index = len(lect_urllist)
            if not args['--quiet']:
                print("\nStarting download of "+str(end_index-start_index) +
                      " lectures")
            for i in range(start_index, end_index):
                dlurl = get_dlurl(lect_urllist[i], login_cookie, dl_format)
                download_file(dlurl, csize=CSIZE, quiet=args['--quiet'])
