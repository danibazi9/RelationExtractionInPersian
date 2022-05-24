from bs4 import BeautifulSoup, Tag
import requests

resultsFile = open("../data/raw/alphabets.txt", "w", encoding="utf8")
url = "https://fa.wikipedia.org/wiki/ویکی‌پدیا:فهرست_سریع"
web = requests.get(url)

soup = BeautifulSoup(web.content, "html5lib")
table = soup.find('table', attrs={'style': 'width: 80%; font-family:monospace; padding: 3px; background: #f7f8ff; border: 1px solid gray; margin: 0 auto;'})
for tr in table.contents[1].contents:
    if isinstance(tr, Tag):
        tds = tr.find_all("td")
        for td in tds:
            resultsFile.write(td.text)
