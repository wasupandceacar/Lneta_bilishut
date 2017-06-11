import requests
import re
import json

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

num=0

lnetas=[]

def shut(av):
    pull(av)

def pull(av):
    print(av)
    url=BILI_URL+str(av)
    data = s.get(url, headers=BILI_HEADERS).content
    #open(PATH, 'wb').write(data)
    ddata=data.decode('utf-8')
    titlelist = re.compile('h1 title="(.*?)">')
    title = re.findall(titlelist, ddata)
    #检验视频是否存在
    if len(title)==0:
        print("视频不存在")
    else:
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
                    print("是啊")
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
                    print("非neta")
            else:
                print("非L难度")
        else:
            print("非东方")

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
    for i in range(1, 500001):
        pull(i)
    print("有"+str(num)+"个Lneta")
    jdata = json.dumps(lnetas, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    f = open(PATH, 'w')
    f.write(jdata)
    f.close()