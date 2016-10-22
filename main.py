import requests
import bs4


def genSoup(url): # gets soup object from url
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    return soup


def getAll(url, soup): # universal retrieval
    preimgsrc = []
    imgsrc = []
    imgtags = soup.select('img')
    for tag in imgtags:
        preimgsrc.append(tag.get('src'))
    domain = url[url.find('/') + 2:] # TODO try this with re
    domain = domain[:domain.find('/')]
    # '''
    atags = soup.select('a')
    for tag in atags:
        if type(tag.get('href')) is str:
            if ('.jpg' or '.png' or '.jpeg') in tag.get('href'): # TODO expand selection criteria with ext list below
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


def download(imgsrc): # iterates over list to download images
    dlcount = 1
    for imgurl in imgsrc:
        print("Downloading", str(dlcount), "of", str(len(imgsrc)))
        imgdata = requests.get(imgurl)
        filename = imgurl[imgurl.rfind('/') + 1:]
        filename = cleanName(filename) # catches errors with invalid file names, often trailing after the extension
        imgfile = open(filename, 'wb')
        for chunk in imgdata.iter_content(10000):
            imgfile.write(chunk)
        imgfile.close()
        dlcount += 1


# TODO make a downloadAll function for ease of use when importing this module

if __name__ == '__main__':
    url = input('URL >>> ')
    soup = genSoup(url)
    print('Generating soup object... '),
    if '4chan' in url:
        print("Downloading with '4chan' function...")
        imgsrc = getChan(url, soup)
    else:
        print("Downloading with universal function...")
        imgsrc = getAll(url, soup)
    download(imgsrc)
    input("Done! Enter to exit.")

