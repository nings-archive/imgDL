# imgDL is a python-CLI script to download images off webpages
# Inspired by youtube-dl
# ningyuan.sg@gmail.com, ningyuan.io

import sys, os
import requests
import bs4
from imgDLmod import *

def download(urls):
    dlcount = 1
    for url in urls:
        print("Downloading {}/{} @ {}".format(str(dlcount), str(len(urls)), url))
        downloadUrl(url)
        dlcount += 1


def main(args):
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
        else:
            download(getAncHref(url))
        print("Downloads completed for {}.\n".format(url))
        os.chdir('..')

main(sys.argv)
