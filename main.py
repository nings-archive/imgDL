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

# gets soup object from url
def getSoup(url):
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    return soup


# universal retrieval
def getAll(url):
    soup = getSoup(url)
    preimgsrc = []
    imgsrc = []
    imgtags = soup.select('img')
    for tag in imgtags:
        preimgsrc.append(tag.get('src'))
    # TODO try this with re
    domain = url[url.find('/') + 2:]
    domain = domain[:domain.find('/')]
    # '''
    atags = soup.select('a')
    for tag in atags:
        if type(tag.get('href')) is str:
            # TODO expand selection criteria with ext list below
            if ('.jpg' or '.png' or '.jpeg') in tag.get('href'):
                preimgsrc.append(tag.get('href'))   
    # '''
    for imgurl in preimgsrc:
        if ('http' or 'https') in imgurl:
            imgsrc.append(imgurl)
        elif imgurl[:2] == '//':
            imgsrc.append('http:' + imgurl)
        elif imgurl[0] == '/' and imgurl[1] != '/':
            imgsrc.append(domain + imgurl)
    return imgsrc


def get4chan(url):
    print("Identified as 4chan thread.")
    soup = getSoup(url)
    selection = soup.select('div .fileText a')
    imgurls = []
    for tag in selection:
        href = 'http:' + tag.get('href')
        imgurls.append(href)
    return imgurls


def getImgur(url):
    # imgur urls types:
    # imgur.com/a/abcdef (multi, single)--'div .post-image a', tag.get('href')
    # imgur.com/gallery/abcdef (multi, single)
    # imgur.com/abcdef (single)
    print("Identified as Imgur post.")


def cleanName(filename):
    exts = ['.jpg', '.jpeg', '.png', '.gif', '.webm', '.tif', '.tiff', '.bmp', '.pbm', '.pgm', '.ppm', '.pnm', '.webp', '.svg']
    for ext in exts:
        if ext in filename.lower():
            filename = filename[:filename.lower().rfind(ext) + len(ext)]
    return filename


# iterates over list to download images
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

