from googleapiclient.discovery import build
import requests
import json
import time

config: dict = json.load(open(".keys.json", 'r'))

KEY = config.get('KEY')
URL = 'https://www.googleapis.com/customsearch/v1'
CX = config.get('CX')

query = 'sloth'

service = build("customsearch", "v1",
               developerKey=KEY)

res = service.cse().list(
    q=query,
    cx=CX,
    searchType='image',
    fileType='.png',
    imgType='clipart',
    num=10,
    safe= 'off',
).execute()

total = res.get('searchInformation').get('totalResults')
total = int(total) if total else -1
pages = total // 10
current = 0
links = []

print('total:', total)
while pages > current:
    links += [
        item.get('link') for item in res.get('items', [])
    ]
    current += 1
    try:
        res = service.cse().list(
            q=query,
            cx=CX,
            searchType='image',
            fileType='.png',
            imgType='clipart',
            num=10,
            safe= 'off',
            start=current * 10
        ).execute()
        print('searching for', current)
    except:
        break
    time.sleep(5)
    if current > 1000:
        break

    

print(links)
for i, link in enumerate(links):
    name = link.split('/')[-1]
    if '.png' not in name:
        name += '.png'
    res = requests.get(link)
    if res.status_code < 400:
        print('now writing', i)
        with open(f'images/{name}', 'wb') as f:
            f.write(res.content)
    time.sleep(1)