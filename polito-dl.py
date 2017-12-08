#!/usr/bin/python3

#Polito Videolessons Downloader 

import os,requests,urllib,re,html,sys


def polito_login(user,passw):
    with requests.session() as s :
        r=s.get('https://idp.polito.it/idp/x509mixed-login')
        r=s.post('https://idp.polito.it/idp/Authn/X509Mixed/UserPasswordLogin',data={'j_username':user,'j_password':passw})
        relaystate=html.unescape(re.findall('name="RelayState".*value="(.*)"',r.text)[0])
        samlresponse=html.unescape(re.findall('name="SAMLResponse".*value="(.*)"',r.text)[0])
        r=s.post('https://www.polito.it/Shibboleth.sso/SAML2/POST',data={'RelayState':relaystate,'SAMLResponse':samlresponse})
        r=s.post('https://login.didattica.polito.it/secure/ShibLogin.php')
        relaystate=html.unescape(re.findall('name="RelayState".*value="(.*)"',r.text)[0])
        samlresponse=html.unescape(re.findall('name="SAMLResponse".*value="(.*)"',r.text)[0])
        r=s.post('https://login.didattica.polito.it/Shibboleth.sso/SAML2/POST',data={'RelayState':relaystate,'SAMLResponse':samlresponse})
        if r.url=="https://didattica.polito.it/portal/page/portal/home/Studente": #Login Successful
            return s.cookies
        else:
            print("Something went wrong with the login...")
            return ""


def extract_video_links(url,login_cookie):
    with requests.session() as s:
        s.cookies=login_cookie
        r=s.get(url) 
    #Different html structure for videolessons on elearning.polito.it and didattica.polito.it
    if "didattica.polito.it" in url:
        links=re.findall('href="(sviluppo\.videolezioni\.vis.*lez=\w*)">',r.text)
        for i in range(len(links)):
            links[i]='https://didattica.polito.it/pls/portal30/'+html.unescape(links[i])
    elif "elearning.polito.it" in url:
        links=re.findall("href='(template_video\.php\?[^']*)",r.text)
        for i in range(len(links)):
            links[i]='https://elearning.polito.it/gadgets/video/'+html.unescape(links[i])
    else:
        print("Sorry, still under developement")
        links=""
    return links


def extract_download_url(url,login_cookie):
    with requests.session() as s:
        s.cookies=login_cookie
        r=s.get(url)
        if "didattica.polito.it" in url:
            d_url=re.findall('href="(.*)".*Video',r.text)[0]
            r=s.get('https://didattica.polito.it'+html.unescape(d_url),allow_redirects=False)
            d_url=r.headers['location']
        elif "elearning.polito.it" in url:
            d_url=re.findall('href="(download.php[^\"]*).*video1',r.text)[0]
            r=s.get('https://elearning.polito.it/gadgets/video/'+html.unescape(d_url),allow_redirects=False)
            d_url=r.headers['location']
        else:
            print("Sorry, still under developement")
            d_url=""  
    return d_url     




def download_video(url,directory):
    filename=url.split('/')[-1]
    print('Download in corso di "'+filename+'"')
    urllib.request.urlretrieve(url,os.path.join(directory,filename))
    
    



try:
    directory=os.path.dirname(os.path.realpath(__file__))
except:
    directory=os.getcwd()
    

if len(sys.argv)<2:
    print("Interactive Mode")
    user=input("Inserisci il tuo nome utente del politecnico: ")
    passw=input("Inserisci la tua password: ")
    video_url=input("Inserisci il link delle videolezioni: ")
else:
    user=sys.argv[1]
    passw=sys.argv[2]
    video_url=sys.argv[3]
    if len(sys.argv)==5:
        directory=sys.argv[4]





#Quick and dirty... horrible code to rewrite in the future
print("Login on the teaching portal...")
lcookie=polito_login(user,passw)
print("Extracting video list...")
links=extract_video_links(video_url,lcookie)
print("\n"+str(len(links))+" videos found")
print("Which videolessons do you want to download? Insert a range, right limit is excluded.")
print("(For example to download all the videos give 1-"+str(len(links)+1)+")")
inp=input("Range:")
inp=re.match("(\d*)-(\d*)",inp)
if inp:
    st=int(inp.groups()[0])
    end=int(inp.groups()[1])
    for i in range(st,end):
        download_video(extract_download_url(links[i-1],lcookie),directory)
else:
    print("Wrong input")



