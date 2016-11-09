import requests
import bs4

# imgDL
# TODO: filter out thumbnails?
# This module contains the following:
# getImgSrc(url) - given a url, returns a list of img srcs (general, universal)
# * this tends to include thumbnails, so is not used by default
# getAncHref(url) - given a url, returns a list of anchor hrefs (general, universal)
# * most sites link to full_res images in anchor tags rather than img
# get4chan(url) - given a 4chan url, returns a list of img srcs (specific, 4chan)

# main will have a list of urls from os' argparse

EXTENSIONS = ('jpeg', 'jpg', 'png', 'svg', 'tif', 'gif', 'webm', 'bmp')

def addHttp(url):
    case_httpdd = r'^http .*'
    case_dd = r'^//'
    case_d = r'^/[^/]'
    case_none = r'^[^http://]'

def cleanUrls(urls, original_url):
    # removes invalid urls (by trailing exts)
    ext_urls = []
    for url in urls:
        if type(url) is str and url.endswith(EXTENSIONS):
            ext_urls.append(url)
    # appends http or http: or http:// or http://domain.com or none accordingly
    new_urls = []
    # TODO: regex for first / that is not //

    domainRe = re.match(r'', domain, re.I)

    domain = original_url[original_url.find('/') + 2:]
    for url in ext_urls:
        if url.startswith('http'):
            new_urls.append(url)
        elif url[:2] == '//':
            new_urls.append('http:' + url)
        elif url[0] == '/' and url[1] != '/':
            new_urls.append(domain + url)
        else:
            new_urls.append('http://' + url)
            # e.g. en.wikipedia.org/wiki/BMP_file_format/wiki/File:BMPfileFormat.png
    return new_urls

# TODO: document error from requests.get, bs4.BeautifulSoup
def getImgSrc(url):
    # generates soup object
    soup = bs4.BeautifulSoup(requests.get(url).text, 'html.parser')
    # generates raw list of src urls
    img_tags = soup.select('img')
    raw_srcs = []
    for tag in img_tags:
        raw_srcs.append(tag.get('src'))
    # clean & return
    img_srcs = cleanUrls(raw_srcs, url)
    return img_srcs

def getAncHref(url):
    # generates soup object
    soup = bs4.BeautifulSoup(requests.get(url).text, 'html.parser')
    # generates raw list of href urls
    anc_tags = soup.select('a')
    raw_hrefs = []
    for tag in anc_tags:
        raw_hrefs.append(tag.get('href'))
    # clean & return
    href_urls = cleanUrls(raw_hrefs, url)
    return href_urls

def get4chan(url):
    # generates soup object
    soup = bs4.BeautifulSoup(requests.get(url).text, 'html.parser')
    # generates raw list of imgs
    anc_tags = soup.select('div .fileText a')
    href_urls = []
    for tag in anc_tags:
        href_urls.append('http:' + tag.get('href'))
    return href_urls

def downloadUrl(url):
    data = requests.get(url)
    name = url[url.rfind('/') + 1:]
    with open(name, 'wb') as new_file:
        for chunk in data.iter_content(10000):
            new_file.write(chunk)
