polito_dl - Command-line script and python module to download Polytechnic of Turin's online lessons from didattica.polito.it and elearning.polito.it


- [Installation](#Installation)
- [Description](#Description)
- [Examples](#Examples)


# Installation
Ubuntu or Debian:

    sudo apt install python3-pip
    pip3 install -r requirements.txt


Windows:  
  
Install [Python](https://www.python.org/downloads/) (don't forget to check the "ADD TO PATH" option).  
Then open the command prompt and type:

    pip3 install -r requirements.txt
  
# Description
**polito_dl** is a script written in Python to download video lessons from didattica.polito.it and elearning.polito.it with a simple and powerful command-line interface. It features a nice download progress bar and possibility to resume downloads.
URL can be the link of a single videolesson or the course's on-line lessons main page.


    Usage:
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


# Examples

    $ ./polito_dl.py "https://didattica.polito.it/pls/portal30/sviluppo.videolezioni.vis?cor=371"
     
    Insert your didattica.polito.it username: s424242
    Insert your didattica.polito.it password: 
     
    Do you want to store your credentials in ~/.config/polito_dl/auth ? [Y/n] y
     
    Starting download of 57 lectures
    Algori..._01.mp4:   4%|█▌                                        | 5.00M/131M [00:01<01:30, 1.38MB/s]


    $ cat cred_file
    ["s424242", "my_p4ssw0rd"]
    $ ./polito_dl.py --auth-file cred_file "https://didattica.polito.it/pls/portal30/sviluppo.videolezioni.vis?cor=371"
     
    Starting download of 57 lectures
    Algori..._01.mp4:   4%|█▌                                        | 5.00M/131M [00:01<01:30, 1.38MB/s]


    $ ./polito_dl.py --list-lectures "https://didattica.polito.it/pls/portal30/sviluppo.videolezioni.vis?cor=371" | more
     
    Lectures list
    1) 2019_Lezione 01
    2) 2019_Lezione 02
    3) 2019_Lezione 03
    4) 2019_Lezione 04
    5) 2019_Lezione 05
    --More--    


    $ ./polito_dl.py --print-syllabus "https://didattica.polito.it/pls/portal30/sviluppo.videolezioni.vis?cor=371" | more
     
    Course: Python Scripting
    Professor: Prof. Mario Rossi
     
    Lectures
    2019_Lezione 01 - 01/10/2018
        Introduzione al corso
     
     
    2019_Lezione 02 - 01/10/2018
        L'essenziale del linguaggio Python (parte 1)
     
     
    --More--






