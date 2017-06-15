import requests
import re
import urllib
import json
import traceback
from threading import Thread

s = requests.Session()

PATH="tmp.json"

HTMLPATH="F:/1.html"

THkey=['红魔乡','妖妖梦','永夜抄','风神录','地灵殿','星莲船','神灵庙','辉针城','绀珠传']

Lkey=['l','lunatic','l难度']

NETAkey2=['nb','nm','no%20bomb','no%20miss','no%20boom','nobomb','nomiss','noboom','nn','nob','禁雷','一命','封印']

NETAkey=['nb','nm','no bomb','no miss','no boom','nobomb','nomiss','noboom','nn','nob','禁','一命','封印']

NOTkey=['innocent','normal','手书','弹幕风','音MAD','东方夜雪神','arrange','被封印的妖怪']

NOTLkey=['normal','list','file','html','replay','reply','locat','blossom','adsl','play','all','非l','clear','love','girl','black']

BILI_HEADERS = {
                'Host': 'www.bilibili.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/50.0.2661.102 Safari/537.36'
            }

SEARCH_HEADERS = {
                'Host': 'search.bilibili.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/50.0.2661.102 Safari/537.36'
            }

BILI_URL = 'http://www.bilibili.com/video/av'

SEARCH_URL = 'http://search.bilibili.com/all?keyword='

PAGE = '&page='

#搜索到的Lneta数
num=0

lnetas=[]

#开始的av号-1
start=0

avs=[]

#线程数
tnum=0

c=0

class MyThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global tnum
        for i in range(start+100000*tnum+1, start+100000*tnum+100001):
            try:
                pull(i)
            except:
                print(i)
                traceback.print_exc()
                continue
        pass

def shut(av):
    pull(av)

def search(key1, key2, key3):
    pagenum=1
    url=SEARCH_URL+ chquote(key1)+'%20'+chquote(key2)+'%20'+chquote(key3)+PAGE+str(pagenum)
    data = s.get(url, headers=SEARCH_HEADERS).content
    #open(HTMLPATH, 'wb').write(data)
    ddata = data.decode('utf-8')
    while('没有相关数据' not in ddata):
        avlist = re.compile('<a href="//www.bilibili.com/video/av(.*?)\?')
        avnum = re.findall(avlist, ddata)
        for num in avnum:
            num=int(num)
            if num not in avs:
                avs.append(num)
        pagenum+=1
        url=SEARCH_URL+ chquote("妖妖梦")+'%20'+chquote('lunatic')+'%20'+chquote('no%20bomb')+PAGE+str(pagenum)
        data = s.get(url, headers=SEARCH_HEADERS).content
        ddata = data.decode('utf-8')

#判断中文
def is_chinese(s):
    if s >= u'\u4e00' and s<=u'\u9fa5':
        return True
    else:
        return False

#转换中文码
def chquote(msg):
    flag=False
    for s in msg:
        if is_chinese(s):
            flag=True
            break
    if flag:
        return urllib.parse.quote(msg)
    else:
        return msg

def pullavs():
    avav=sorted(avs)
    for avnum in avav:
        pull(avnum)

def pull(av):
    url=BILI_URL+str(av)
    data = s.get(url, headers=BILI_HEADERS).content
    #open(HTMLPATH, 'wb').write(data)
    ddata=data.decode('utf-8')
    titlelist = re.compile('h1 title="(.*?)">')
    title = re.findall(titlelist, ddata)
    #检验视频是否存在
    if len(title)!=0:
        taglist = re.compile('<a class="tag-val" href=".*?title="(.*?)" target="_blank"')
        tags = re.findall(taglist, ddata)
        title=title[0]
        commentlist = re.compile('v_desc">(.*?)</div>', re.S)
        comment=re.findall(commentlist, ddata)
        if len(comment)==0:
            comment=""
        else:
            comment = washComment(comment[0])
        if isTouhou(title, tags, comment):
            lcomment=washLComment(comment)
            ltitle=washLComment(title)
            if isLunatic(ltitle, tags, lcomment):
                if isNeta(title, tags, comment):
                    print(str(av)+" Lneta")
                    global num
                    num+=1
                    lneta={}
                    lneta['av'] = av
                    namelist = re.compile('author" content="(.*?)"')
                    name = re.findall(namelist, ddata)
                    if len(name)==0:
                        name=""
                    else:
                        name=name[0]
                    lneta['name'] = name
                    timelist = re.compile('datetime=".*?"><i>(.*?)</i>')
                    time = re.findall(timelist, ddata)
                    if len(time)==0:
                        time=""
                    else:
                        time=time[0]
                    lneta['time'] = time
                    lneta['work'] = ""
                    lneta['type'] = ""
                    lneta['comment'] = comment
                    lnetas.append(lneta)
    else:
        print(str(av)+" 不存在")

def pullignore(av):
    url=BILI_URL+str(av)
    data = s.get(url, headers=BILI_HEADERS).content
    #open(HTMLPATH, 'wb').write(data)
    ddata=data.decode('utf-8')
    titlelist = re.compile('h1 title="(.*?)">')
    title = re.findall(titlelist, ddata)
    #检验视频是否存在
    if len(title)!=0:
        taglist = re.compile('<a class="tag-val" href=".*?title="(.*?)" target="_blank"')
        tags = re.findall(taglist, ddata)
        title=title[0]
        commentlist = re.compile('v_desc">(.*?)</div>', re.S)
        comment=re.findall(commentlist, ddata)
        if len(comment)==0:
            comment=""
        else:
            comment = washComment(comment[0])
        print(str(av) + " Lneta")
        global num
        num += 1
        lneta = {}
        lneta['av'] = av
        namelist = re.compile('author" content="(.*?)"')
        name = re.findall(namelist, ddata)
        if len(name) == 0:
            name = ""
        else:
            name = name[0]
        lneta['name'] = name
        timelist = re.compile('datetime=".*?"><i>(.*?)</i>')
        time = re.findall(timelist, ddata)
        if len(time) == 0:
            time = ""
        else:
            time = time[0]
        lneta['time'] = time
        lneta['work'] = ""
        lneta['type'] = ""
        lneta['comment'] = comment
        lnetas.append(lneta)
    else:
        print(str(av)+" 不存在")

#判断是否东方相关
def isTouhou(title, tags, comment):
    if isTH(title):
        return True
    for tag in tags:
        if isTH(tag):
            return True
    if isTH(comment):
        return True
    return False

def isTH(msg):
    for key in THkey:
        if key in msg:
            return True
    return False

#判断是否为L难度
def isLunatic(title, tags, comment):
    if isL(title):
        return True
    for tag in tags:
        if isL(tag):
            return True
    if isL(comment):
        return True
    return False

def isL(msg):
    if "l" in msg:
        return True
    if "最高难度" in msg:
        return True
    return False

#判断是否为neta
def isNeta(title, tags, comment):
    if isN(title)==1:
        return True
    for tag in tags:
        if isN(tag)==1:
            return True
        elif isN(tag)==-1:
            return False
    if isN(comment)==1:
        return True
    return False

def isN(msg):
    lomsg=msg.lower()
    for key in NOTkey:
        if key in lomsg:
            return -1
    for key in NETAkey:
        if key in lomsg:
            return 1
    return 0

#去除简介中的html标签
def washComment(msg):
    dr = re.compile(r'<[^>]+>', re.S)
    return dr.sub('', msg)

#去除带l的东西
def washLComment(msg):
    lo=msg.lower()
    for key in NOTLkey:
        lo=lo.replace(key, '')
    return lo

if __name__=="__main__":
    '''knum=0
    for key1 in THkey:
        for key2 in Lkey:
            for key3 in NETAkey2:
                try:
                    search(key1, key2, key3)
                    knum+=1
                    print(knum)
                except:
                    traceback.print_exc()
                    continue
    pullavs()'''
    pullignore(2350958)
    pullignore(10306723)
    pullignore(10684206)
    pullignore(10812027)
    pullignore(10812543)
    pullignore(11129763)
    print("有"+str(num)+"个Lneta")
    jdata = json.dumps(lnetas, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    f = open(PATH, 'w',encoding='utf-8')
    f.write(jdata)
    f.close()