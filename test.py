import requests
import datetime
from urllib.parse import urlparse
import re
import html

def remove_tag(content):
   cleanr =re.compile('<.*?>')
   cleantext = re.sub(cleanr, '', content)
   cleantext = html.unescape(cleantext)
   return cleantext

def get_api_result(keyword, display, start):
    url = "https://openapi.naver.com/v1/search/blog?query=" + keyword + "&display=" + str(display) + "&start=" + str(start)
    result = requests.get(urlparse(url).geturl(),
                          headers={"X-Naver-Client-Id": "wYRlTYlyvgQCJJ3lxZzo",
                                   "X-Naver-Client-Secret": "B0cwT7BY6j"})

    return result.json()

def call_and_print(keyword, page):
    json_obj = get_api_result(keyword, 100, page)

    count = 1
    for item in json_obj['items']:
        title = remove_tag(item['title'])
        description = remove_tag(item['description'])
        postdate = datetime.datetime.strptime(item['postdate'], "%Y%m%d").date()
        bloggername = remove_tag(item['bloggername'])

        print("================================================================")
        print(count)
        print(title)
        print(item['link'])
        print(description)
        print(postdate)
        print(item['bloggername'])

        count += 1

keyword = "강남역"
call_and_print(keyword, 1)