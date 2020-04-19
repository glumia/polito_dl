![Test](https://github.com/glumia/polito_dl/workflows/Test/badge.svg?branch=master)
![Flake8 & Black](https://github.com/glumia/polito_dl/workflows/Flake8%20&%20Black/badge.svg)

polito_dl - Command-line tool and library to download Polytechnic of Turin's online 
lessons from didattica.polito.it


- [Installation](#Installation)
- [Description](#Description)


# Installation
Ubuntu or Debian:

    pip3 install polito_dl


Windows:  
  
Install [Python](https://www.python.org/downloads/) (don't forget to check the "ADD TO 
PATH" option).  
Then open the command prompt and type:

    pip3 install polito_dl
  
# Description
polito_dl is a CLI tool and python libray to download video lessons from 
didattica.polito.it with a simple and powerful command-line interface. It features a 
download progress bar and possibility to resume downloads.  
URL can be the link of a single videolesson or the course's on-line lessons main page.


### CLI Interface
```
$ polito_dl
Usage: polito_dl [OPTIONS] COMMAND [ARGS]...

Options:
  --username TEXT  Do not prompt for username.
  --password TEXT  Do not prompt for password. (Warning: this could be
                   insecure, use it only if you know what you are doing.)

  --help           Show this message and exit.

Commands:
  download           Download lecture(s).
  print-course-json  Print course information in JSON format.


```

#### Download lectures
```
$ polito_dl download --help
Usage: polito_dl download [OPTIONS] URL

  Download lecture(s).

Options:
  --all                          Download all course's lectures.
  --format [video|iphone|audio]  Select media format to download (default:
                                 video).

  --chunk-size INTEGER           Set downloader chunk size (default: 1MB).
  --help                         Show this message and exit.

$ polito_dl download "https://didattica.polito.it/portal/pls/portal/sviluppo.videolezioni.vis?cor=456&arg=Lezioni on-line&lez=19649"
Username: s424242
Password: 
Algoritmi_e_programmazione_lez_02.mp4  [##################------------------]   52%  00:00:04
```

#### Print course information
```
$ polito_dl print-course-json --help
Usage: polito_dl print-course-json [OPTIONS] URL

  Print course information in JSON format.

Options:
  --help  Show this message and exit.

$ polito_dl print-course-json "https://didattica.polito.it/portal/pls/portal/sviluppo.videolezioni.vis?cor=456&arg=Lezioni on-line&lez=19649"
Username: s424242
Password: 
{
    "name": "Algoritmi e programmazione",
    "professor": "Paolo Enrico CAMURATI",
    "lectures": [
        {
            "name": "2020_Lezione 01",
            "date": "30/09/2019",
            "path": "sviluppo.videolezioni.vis?cor=456&arg=Lezioni%20on-line&lez=19638",
            "topics": [
                "Introduzione al corso"
            ]
        },
        {
            "name": "2020_Lezione 02",
            "date": "30/09/2019",
            "path": "sviluppo.videolezioni.vis?cor=456&arg=Lezioni%20on-line&lez=19649",
            "topics": [
                "L'essenziale del linguaggio C (parte 1)"
            ]
        },
    ]
}
```

### Python library
Check `polito_dl/client.py`.
