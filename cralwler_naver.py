import requests
import datetime
import re
import html
import db_context
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import OrderedDict
from itertools import count

# Naver 검색 API 이용
def get_api_result(keyword, display, start):
    url = "https://openapi.naver.com/v1/search/blog?query=" + keyword + "&display=" + str(display) + "&start=" + str(start)
    result = requests.get(urlparse(url).geturl(),
                          headers={"X-Naver-Client-Id": "Secret",
                                   "X-Naver-Client-Secret": "Secret"})

    return result.json()

# HTML 태그 제거
def remove_tag(content):
   cleanr =re.compile('<.*?>')
   cleantext = re.sub(cleanr, '', content)
   cleantext = html.unescape(cleantext)
   return cleantext

# 출력, 불러오기
def call_and_print(keyword, page):
    json_obj = get_api_result(keyword, 100, page)
    
    if int(json_obj['total']) <= page - 1:
        temp = []
        return temp, temp, temp, temp, temp, int(json_obj['total'])
    
    title_array = []
    link_array = []
    context_array = []
    date_array = []
    nicname_array = []

    count = 1
    for item in json_obj['items']:
        title = remove_tag(item['title'])
        description = remove_tag(item['description'])
        postdate = datetime.datetime.strptime(item['postdate'], "%Y%m%d").date()
        bloggername = remove_tag(item['bloggername'])

        # print("================================================================")
        # print("ID : " + str(page + count - 1))
        # print("제목 : " + title)
        title_array.append(title)

        # print("링크 : " + item['link'])
        link_array.append(item['link'])

        # print("이미지 링크 : null")
        # print("이미지 개수 : 0")

        # print("내용(간략) : " + description)
        context_array.append(description)

        # print("날짜 : " + str(postdate))
        date_array.append(postdate)
        
        # print("닉네임 : " + bloggername)
        nicname_array.append(bloggername)
        # print("")

        count += 1

    return title_array, link_array, context_array, date_array, nicname_array, int(json_obj['total'])

def naver_content_cralwler(url):
    hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
    param = { 'where': 'post' }

    try:
        response = requests.get(url, params=param, headers=hrd)
        soup_temp = BeautifulSoup(response.text, 'html.parser')
        area_temp = soup_temp.find(id='screenFrame')
        url2 = area_temp.get("src")
    except:
        try:
            area_temp = soup_temp.find(id='mainFrame')
            url3 = area_temp.get("src")
            url4 = "https://blog.naver.com" + url3
            return url4
        except:
            return ""
    
    try:
        response = requests.get(url2, params=param, headers=hrd)
        soup_temp = BeautifulSoup(response.text, 'html.parser')
        area_temp = soup_temp.find(id='mainFrame')
        url3 = area_temp.get("src")
        url4 = "https://blog.naver.com" + url3
        return url4
    except:
        return ""

    return ""

def naver_content_text_cralwler(url):
    hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
    param = { 'where': 'post' }

    try:
        response = requests.get(url, params=param, headers=hrd)
        soup_temp = BeautifulSoup(response.text, 'html.parser')
        area_temp = soup_temp.find_all("div", {"class" : "sect_dsc"})
        img_temp = soup_temp.find_all("div", {"id" : "postListBody"})
        
        for tag2 in area_temp:
            text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', tag2.text)
            text2 = re.sub('\n\n', '', text1)
            text3 = re.sub('<.+?>', '', text2, 0).strip()
            return " ".join(text3.split()), str(img_temp).count("<img")
    except:
        return "", 0

    try:
        area_temp = soup_temp.find_all("div", {"id" : "postViewArea"})
        img_temp = soup_temp.find_all("div", {"id" : "postListBody"})
        
        for tag2 in area_temp:
            text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', tag2.text)
            text2 = re.sub('\n\n', '', text1)
            text3 = re.sub('<.+?>', '', text2, 0).strip()
            return " ".join(text3.split()), str(img_temp).count("<img")
    except:
        return "", 0

    try:
        area_temp = soup_temp.find_all("div", {"class" : "se-main-container"})
        img_temp = soup_temp.find_all("div", {"id" : "postListBody"})
        
        for tag2 in area_temp:
            text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', tag2.text)
            text2 = re.sub('\n\n', '', text1)
            text3 = re.sub('<.+?>', '', text2, 0).strip()
            return " ".join(text3.split()), str(img_temp).count("<img")
    except:
        return "", 0

    return "", 0

# API 검색 세팅
def api_setting(conn, input_search):
    title_array = []
    link_array = []
    context_array = []
    date_array = []
    nicname_array = []
    img_array = []
    img_numx = []
    data_array = []

    total = 0

    for x in range(1, 100, 100):
        try:
            title_temp, link_temp, context_temp, date_temp, nicname_temp, cnt = call_and_print(input_search, x)
            if len(title_temp) > 0:
                title_array.extend(title_temp)
                link_array.extend(link_temp)
                context_array.extend(context_temp)
                date_array.extend(date_temp)
                nicname_array.extend(nicname_temp)
                total = cnt
        except:
            pass
    
    cnt = 0
    if total > 100:
        cnt = 100
    else:
        cnt = total

    for x in range(cnt):
        final_url = naver_content_cralwler(link_array[x])
        data_context, img_numx_temp = naver_content_text_cralwler(final_url)
        data_array.append(data_context)
        img_numx.append(img_numx_temp)
        img_array.append("null")

        print("=================================================================")
        print("ID : " + str(x+1))
        print("제목 : " + title_array[x])
        print("링크 : " + link_array[x])
        print("이미지 링크 : " + img_array[x])
        print("이미지 개수 : " + str(img_numx[x]))
        print("내용(간략) : " + context_array[x])
        print("날짜 : " + str(date_array[x]))
        print("닉네임 : " + nicname_array[x])
        print("내용 길이 : " + str(len(data_array[x])))
        print("")
    
        db_context.insert(conn, str(x+1), str(title_array[x]), str(link_array[x]), 
            str(img_numx[x]), str(context_array[x]), str(date_array[x]), str(nicname_array[x]), "미판정", "미판정", "미판정")
    
    return cnt, title_array, link_array, img_array, img_numx, context_array, data_array, date_array, nicname_array