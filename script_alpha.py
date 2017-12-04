#!/usr/bin/python

import sys
import requests
import html
import urllib



payload = {'j_username':sys.argv[1],'j_password':sys.argv[2]}
video_url=sys.argv[3]
#directory=sys.argv[4]     #Attenzione, path completo!
#if directory[-1]!='/':
#    directory=directory+'/'



with requests.Session() as s:
    p=s.get('https://idp.polito.it/idp/x509mixed-login')
    p=s.post('https://idp.polito.it/idp/Authn/X509Mixed/UserPasswordLogin', \
    	data=payload)
    string=p.text
    start=string.find('action="')+8
    end=string.find('"',start)
    url=string[start:end]
    url=html.unescape(url)                 
    start=string.find('value="',end)+7  
    end=string.find('"/>',start)
    relaystate=string[start:end]
    relaystate=html.unescape(relaystate)
    start=string.find('value="',end)+7
    end=string.find('"/>',start)
    samlresponse=string[start:end]
    samlresponse=html.unescape(samlresponse)
    payload = {'RelayState':relaystate, 'SAMLResponse':samlresponse}
    p=s.post(url, data=payload)
    p=s.get('https://login.didattica.polito.it/secure/ShibLogin.php')
    string=p.text
    start=string.find('action="')+8
    end=string.find('"',start)
    url=string[start:end]
    url=html.unescape(url)                 #Non so perche ma bisogna ripetere due volte
    start=string.find('value="',end)+7     #questo bizzarro procedimento
    end=string.find('"/>',start)
    relaystate=string[start:end]
    relaystate=html.unescape(relaystate)
    start=string.find('value="',end)+7
    end=string.find('"/>',start)
    samlresponse=string[start:end]
    samlresponse=html.unescape(samlresponse)
    payload = {'RelayState':relaystate, 'SAMLResponse':samlresponse}
    p=s.post(url, data=payload)
    #A questo punto il login e' andato a buon fine e posso iniziare a navigare nelle
    #pagine "private" del politecnico
    end=video_url.find('/',video_url.find('//')+2)
    root_url=video_url[:end]
    #Isolo la parte che mi interessa della stringa per poi estrarre i link
    p=s.get(video_url)
    string=p.text
    start=string.find("Lezioni on-line")
    end=string.find("</div>",start)
    string=string[start:end]
    url_list=[]
    start=0
    end=0
    temp=-1
    while start>temp:
        temp=start
        start=string.find('<a href="',end)+9
        end=string.find('">',start)
        url_list.append(string[start:end])
    del url_list[len(url_list)-1]
    for i in range(len(url_list)):
        url_list[i]=html.unescape(url_list[i])
    #A questo punto ho la mia bella lista di url alle videolezioni
    download_list=[]
    for link in url_list:
        p=s.get(root_url+link)
        string=p.text
        start=string.find("Download")
        start=string.find('href="',start)+6
        end=string.find('">',start)
        download_list.append(string[start:end])
    for i in range(len(download_list)):
        download_list[i]=html.unescape(download_list[i])
        download_list[i]=root_url+download_list[i]
    #Prima di scaricare i video con urllib.request.urlretrieve
    #devo ottenere i link a cui vengo reindirizzato con quelli attuali
    #altrimenti non riesco a tirare fuori i nomi dei file
        p=s.get(download_list[i],allow_redirects=False)
        download_list[i]=p.headers['location']
    #E adesso mi scarico i file
    for i in range(60):
        print('\n') #Pulisco il terminale
    if len(sys.argv)>5:
        ran=sys.argv[5].split('-')
        for i in range(len(ran)):
            ran[i]=int(ran[i])
        if len(ran)>1:
            ran=range(ran[0],ran[1])
        else:
            ran=range(ran[0],len(download_list))
    else:
        ran=range(len(download_list))
    downloaded=1;
    for i in ran:
        filename=download_list[i].split('/')[-1]
        print("Download in corso di '%s' - File %d di %d"% (filename,downloaded,len(ran)), end='\r')
        urllib.request.urlretrieve(download_list[i],"C:\\"+filename)
        downloaded+=1
        

print('\n\nDownload videolezioni completato\n\n\n')


