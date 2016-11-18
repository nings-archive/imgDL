import requests, bs4, urllib

IMG_EXTS = ('jpg', 'jpeg', 'png', 'bmp', 'svg', 'gif', 'gifv', 'webm')

def get(url, mode):
    html = requests.get(url)
    print("Getting html...")
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    print("Getting soup...")
    img_urls = []
    if 'a' in mode:
        print("Starting 'a' mode")
        anc_soup = soup.select('a')
        anc_tags = [tag for tag in anc_soup if type(tag.get('href')) is str]
        for tag in anc_tags:
            tag_url = tag.get('href')
            print("Checking {}, endswith is {}".format(
                tag_url, str(tag_url.lower().endswith(IMG_EXTS))))
            if tag_url.lower().endswith(IMG_EXTS):
                img_urls.append(urllib.parse.urljoin(url, tag_url))
    if 'i' in mode:
        print("Starting 'i' mode")
        img_soup = soup.select('img')
        img_tags = [tag for tag in img_soup if type(tag.get('src')) is str]  # redundant?
        for tag in img_tags:
            tag_url = tag.get('src')
            print("Checking {}, endswith is {}".format(
                tag_url, str(tag_url.lower().endswith(IMG_EXTS))))
            if tag_url.lower().endswith(IMG_EXTS):
                img_urls.append(urllib.parse.urljoin(url, tag_url))
    return img_urls

if __name__ == '__main__':
    url = input(' url >>> ')
    results = get(url, 'ai')
    print(results)
    print("---OUTPUT---")
    for url in results:
        print(url)
