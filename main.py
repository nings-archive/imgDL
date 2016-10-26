# imgDL is a python-CLI script to download images off webpages
# Inspired by youtube-dl
# ningyuan.sg@gmail.com, ningyuan.io

import sys, os, time
try:
    import requests
except ImportError:
    sys.stderr.write("ERROR: requests is not installed. This is a requirement for imgDL.\n")
    sys.stderr.flush()
    time.sleep(2)
    exit()
try:
    import bs4
except ImportError:
    sys.stderr.write("ERROR: bs4 is not installed. This is a requirement for imgDL.\n")
    sys.stderr.flush()
    time.sleep(2)
    exit()
try:
    import selenium.webdriver as webdriver
except ImportError:
    sys.stderr.write("ERROR: Selenium is not installed. This is a requirement for imgur links.")
    sys.stderr.flush()
    time.sleep(2)

# TODO: Clean the code, one function for each site
# TODO: allow sys.argv
# TODO: fix errors with unreliable web links, conditionals need to be more strict
# TODO: change file name, or at least main.exe to imgDL.exe

def getSoup(url):
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    return soup


def getAll(url):
    soup = getSoup(url)
    preimgsrc = []
    imgsrc = []
    imgtags = soup.select('img')
    for tag in imgtags:
        preimgsrc.append(tag.get('src'))
    domain = url[url.find('/') + 2:] # TODO try this with re
    domain = domain[:domain.find('/')]
    '''
    atags = soup.select('a')
    for tag in atags:
        if type(tag.get('href')) is str:
            if ('.jpg' or '.png' or '.jpeg') in tag.get('href'): 
            # TODO expand selection criteria with ext list below
                preimgsrc.append(tag.get('href'))   
    '''
    for imgurl in preimgsrc:
        if ('http' or 'https') in imgurl:
            imgsrc.append(imgurl)
        elif imgurl[:2] == '//':
            imgsrc.append('http:' + imgurl)
        elif imgurl[0] == '/' and imgurl[1] != '/':
            imgsrc.append(domain + imgurl)
    return imgsrc


def getChan(url, soup): # retrieves imgsrc list of img URLS for 4chan
    fileText = soup.select('div .fileText a')
    imgsrc = []
    for tag in fileText:
        src = 'http:' + tag.get('href')
        imgsrc.append(src)
    return imgsrc


def cleanName(filename): # sanitises file names for OS module
    exts = ['.jpg', '.jpeg', '.png', '.gif', '.webm', '.tif', '.tiff', '.bmp', '.pbm', '.pgm', '.ppm', '.pnm', '.webp', '.svg']
    for ext in exts:
        if ext in filename.lower():
            filename = filename[:filename.lower().rfind(ext) + len(ext)]
    return filename


def download(imgurls):
    dlcount = 1
    for imgurl in imgurls:
        print("Downloading {}/{} @ {}".format(str(dlcount), str(len(imgurls)), imgurl))
        data = requests.get(imgurl)
        name = imgurl[imgurl.rfind('/') + 1:]
        with open(name, 'wb') as imgfile:
            for chunk in data.iter_content(10000):
                imgfile.write(chunk)
        dlcount += 1


def main(args):
    if len(args) > 2:
        multi = True

    for url in args[1:]:
        dirname = url[url.rfind('/') + 1:]
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        os.chdir(dirname)

        if 'http' in url:
            None
        elif 'www' in url:
            url = 'http://' + url
        else:
            url = 'http://www.' + url
        print("Downloading from", url)

        if 'boards.4chan.org' in url:
            download(get4chan(url))
        elif 'imgur.com' in url:
            download(getImgur(url))
        elif 'reddit.com' in url:
            (getReddit(url))
        print("Downloads completed for {}.\n".format(url))
        os.chdir('..')

main(sys.argv)
