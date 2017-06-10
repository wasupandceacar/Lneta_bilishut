import requests
import re
import os

s = requests.Session()

PATH="F://1.html"

BILI_HEADERS = {
                'Host': 'www.bilibili.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/50.0.2661.102 Safari/537.36'
            }

BILI_URL = 'http://www.bilibili.com/video/av'

def shut(av):
    pull(av)

def pull(av):
    url=BILI_URL+str(av)
    data = s.get(url, headers=BILI_HEADERS).content
    ddata=data.decode('utf-8')
    taglist = re.compile('<a class="tag-val" href=".*?title="(.*?)" target="_blank"')
    tags = re.findall(taglist, ddata)
    titlelist = re.compile('h1 title="(.*?)">')
    title = re.findall(titlelist, ddata)[0]
    commentlist = re.compile('v_desc">(.*?)</div>', re.S)
    comment = re.findall(commentlist, ddata)[0]

if __name__=="__main__":
    shut(11173683)