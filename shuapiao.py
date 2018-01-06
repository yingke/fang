# coding=utf-8
'''
   2017年12月21日 21点50分
 “恒大龙庭最帅置业顾问评选大赛”竞赛刷票插件

'''
import requests
import json
import time
import re
import  random
from random import choice
from bs4 import BeautifulSoup
import threading
import sys
import datetime

# r = requests.get('http://api.xicidaili.com/free2016.txt')
# print (type(r))
# print (r.status_code)
# print (r.encoding)
# print (r.text)
# print (r.cookies)

uas = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
    ]

# 请求头信息
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '29',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'survey.fang.com',
    'Origin': 'http://m.fang.com',
    'Referer': 'http://m.fang.com/zt/wap/201712/zuishuaihengda.html?city=hd&m=xfdg&from=singlemessage',
    'User-Agent': choice(uas),
    'X-Requested-With': 'XMLHttpRequest'
}


def get_ip():
    '''获取代理IP'''
    all_url = []  # 存储IP地址的容器
    url = 'http://www.xicidaili.com/nt'
    my_headers = {
        'Accept': 'text/html, application/xhtml+xml, application/xml;',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Referer': 'http: // www.xicidaili.com/nn',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 45.0.2454.101Safari / 537.36'
    }
    r = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(r.text,'html.parser')
    data = soup.find_all('td')

    #定义IP和端口Pattern规则
    ip_compile = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  #匹配IP
    port_compile = re.compile(r'<td>(\d+)</td>')  #匹配端口
    ip = re.findall(ip_compile,str(data))    #获取所有IP
    port = re.findall(port_compile,str(data))  #获取所有端口
    z = [':'.join(i) for i in zip(ip,port)]  #列表生成式
    
    return z


def toupiao(url,code=0,ips=[]):

    x=random.randint(10,40)
    y=random.randint(10,30)
    print(x)
    params = {'q_29880[]':13933,'x':x,'y':y}
    try:
        ip=choice(ips)
        print(ip.text)
    except:
        return False
    else:
        # 指定IP
        proxies = {
            'http': ip
        }
    try:
        result = requests.post(url=url, data=params, proxies=proxies, )


    except requests.exceptions.ConnectionError:
        print( 'ConnectionError')
        if not ips:
            print( 'ip 已失效')
            sys.exit()
        # 删除不可用的代理IP
        if ip in ips:
            ips.remove(ip)
        # 重新请求url
            toupiao(url=url, code=0, ips=[])
    else:
        date = datetime.datetime.now().strftime('%H:%M:%S')
        print( u"第%s次 [%s] [%s]：投票%s (剩余可用代理IP数：%s)" % (code, date, ip, result.text, len(ips)))



def gorun():
    ips = []
    posturl = "http://survey.fang.com/web/poll_simple.php?survey_id=66786"
    # xrange() 生成的是一个生成器

    for i in range(6000):
        print(i)
        # 每隔1000次重新获取一次最新的代理IP，每次可获取最新的100个代理IP
        if i % 1000 == 0:
            ips.extend(get_ip())
            print( '--------------------------------------')
            print(ips)
        # 启动线程，每隔1s产生一个线程，可通过控制时间加快投票速度
        t1 = threading.Thread(target=toupiao, args=(posturl, i, ips))
        t1.start()
        time.sleep(60)  # time.sleep的最小单位是毫秒


def toshuapiao():
    count = 0  # 计数器
    while count < 4000:
        all_url = get_ip()
        for i in all_url:
            proxies = {"http": i}
            x = random.randint(10, 40)
            y = random.randint(10, 30)
            print(x)
            params = {'q_29880[]': 13933, 'x': x, 'y': y}

            try:
                posturl = "http://survey.fang.com/web/poll_simple.php?survey_id=66786"
                r = requests.post(url=posturl, data=params, headers=headers, proxies=proxies)
                # if (r.json()['flag'] == True):
                count += 1
                #     print("成功投票%d次！" % (count))
                print(r.text)
            except Exception as reason:
                print("错误原因是：", reason)

        if count % 100 == 0:
            all_url.extend(get_ip())
            print('--------------------------------------')





if __name__ == '__main__':
    toshuapiao()








