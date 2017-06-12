import requests
import re
import json
import traceback
from threading import Thread

s = requests.Session()

PATH="1.json"

THkey=['红魔乡','妖妖梦','永夜抄','风神录','地灵殿','星莲船','神灵庙','辉针城','绀珠传']

NETAkey=['nb','nm','no bomb','no miss','no boom','nobomb','nomiss','noboom','nn','nob','禁','一命','封印']

NOTkey=['innocent']

BILI_HEADERS = {
                'Host': 'www.bilibili.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/50.0.2661.102 Safari/537.36'
            }

BILI_URL = 'http://www.bilibili.com/video/av'

#搜索到的Lneta数
num=0

lnetas=[]

#开始的av号-1
start=1000000

#线程数
tnum=0

class MyThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
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

def pull(av):
    url=BILI_URL+str(av)
    print(av)
    data = s.get(url, headers=BILI_HEADERS).content
    #open(PATH, 'wb').write(data)
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
            if isLunatic(title, tags, comment):
                if isNeta(title, tags, comment):
                    print(str(av)+"  是啊")
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
    if "l" in msg.lower():
        return True
    if "最高难度" in msg:
        return True
    return False

#判断是否为neta
def isNeta(title, tags, comment):
    if isN(title):
        return True
    for tag in tags:
        if isN(tag):
            return True
    if isN(comment):
        return True
    return False

def isN(msg):
    lomsg=msg.lower()
    for key in NOTkey:
        if key in lomsg:
            return False
    for key in NETAkey:
        if key in lomsg:
            return True
    return False

#去除简介中的html标签
def washComment(msg):
    dr = re.compile(r'<[^>]+>', re.S)
    return dr.sub('', msg)

if __name__=="__main__":
    threads=[]
    global tnum
    for i in range(30):
        thread=MyThread()
        threads.append(thread)
    for i in range(len(threads)):
        tnum=i
        threads[i].start()
    for thread in threads:
        thread.join()
    print("有"+str(num)+"个Lneta")
    jdata = json.dumps(lnetas, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    f = open(PATH, 'w')
    f.write(jdata)
    f.close()
