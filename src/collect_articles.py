from bs4 import BeautifulSoup, Tag
import requests
import json
import time

from requests.adapters import HTTPAdapter
from urllib3 import Retry

hrefs = open('../data/raw/hrefs.txt', 'r', encoding="utf8")
results = open('../data/raw/raw_dataset.json', 'w', encoding="utf8")
dataset = []

line = 1
count = 1
start_time = time.time()

for href in hrefs.read().splitlines():
    if line % 4 == 1:
        try:
            # send a request to website
            web = requests.get(href)
        except:
            # handle a problem that too requests to a website that gives us max_retries error
            # This block code will get the url and retry 3 times if it gets error
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            web = requests.get(href)

        soup = BeautifulSoup(web.content, "html5lib")
        title = soup.find('h1', attrs={'id': 'firstHeading'}).text
        div = soup.find('div', attrs={'class': 'mw-parser-output'})

        final_text = ''
        for p_tag in div.findChildren("p", recursive=False):
            p_text = ''
            for element in p_tag.contents:
                if isinstance(element, Tag):
                    if element.name != 'sup' and element.name != 'br':
                        if 'می‌توانید با گسترش آن به ویکی‌پدیا کمک کنید' not in element.text \
                                and element.text.replace('\n', '') != '':
                            p_text += element.text
                else:
                    if 'می‌توانید با گسترش آن به ویکی‌پدیا کمک کنید' not in element \
                            and element.replace('\n', '') != '':
                        p_text += element

            text = p_text.replace('\n', '')
            if p_text != '':
                final_text += p_text + ' '

        dataset.append({'id': count, 'title': title, 'text': final_text})
        count += 1

    print(str(line) + " from 8998 (", end='')
    print("%4.2f"%((line / 8998) * 100), end='')
    print("%)")
    line += 1

results.write(json.dumps(dataset, ensure_ascii=False))
results.close()

end_time = time.time()
print("\nTime of execution: ")
print("%5.2f"%((end_time - start_time) / 60), end='')
print(" minutes")
