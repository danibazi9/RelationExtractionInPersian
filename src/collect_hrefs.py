from bs4 import BeautifulSoup, Tag
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import urllib

def func():
    url = "https://fa.wikipedia.org/wiki/ویژه:تمام_صفحه‌ها?"
    alphabets = open('../data/raw/alphabets.txt', 'r', encoding="utf8")
    hrefs = open('../data/raw/hrefs.txt', 'w', encoding="utf8")
    count = 1

    for alphabet in alphabets.read().splitlines():
        if len(alphabet) == 1:
            try:
                # send a request to website
                web = requests.get(url + 'from=' + alphabet + '&to=&namespace=0')
            except:
                # handle a problem that too requests to a website that gives us max_retries error
                # This block code will get the url and retry 3 times if it gets error
                session = requests.Session()
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)

                web = requests.get(url + 'from=' + alphabet + '&to=&namespace=0')

            soup = BeautifulSoup(web.content, "html5lib")
            table = soup.find('ul', attrs={'class': 'mw-allpages-chunk'})
            for tr in table.contents:
                if isinstance(tr, Tag):
                    aas = tr.find_all("a")
                    for a in aas:
                        if 'ابهام' not in a.text and '-' not in a.text and '(' not in a.text and ')' not in a.text:
                            hrefs.write(urllib.parse.unquote('https://fa.wikipedia.org' + a.attrs['href']) + "\n")

        print(str(count) + " from 1122 (", end='')
        print("%4.2f"%((count / 1122) * 100), end='')
        print("%)")
        count += 1


if __name__ == "__main__":
    print("hrefs collected")