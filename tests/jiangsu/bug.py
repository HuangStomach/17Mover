# -*- coding: UTF-8 -*-
import re
import sys
import time
import urlparse
import pyjsonrpc
from urllib import urlopen
from bs4 import BeautifulSoup

def iconv(str, code = 'utf8'):
    if (str is None or len(str) == 0):
        return ''
    else:
        return str.encode(code)

reload(sys)
sys.setdefaultencoding('utf-8')

j = 1
file = open('retry.txt', 'a')
base = "http://www.yqgx.org/"

while 1 == 1:
    html = urlopen(base + "inst_list.asp?currentpage=" + str(j) + "&p=0&username=&inst_name=&inst_type=&inst_yt=&classid=&lyid=&inst_jszb=&areaid=&user_id=")
    doc = BeautifulSoup(html.read(), "html5lib")

    yiqikong = pyjsonrpc.HttpClient(
        url = "http://directory.17kong.com/api"
        #url = "http://192.168.0.5:5021/api"
    )
        
    links = doc.findAll(href = re.compile('inst_show.asp'))
        
    if (len(links) == 0):
        break

    for link in links:
        try:
            equipment = {}
            href = base + link['href']
            #仪器名称
            equipment['name'] = iconv(link.string)
            print equipment['name']
            #仪器来源
            equipment['source_name'] = iconv('江苏省大型科学仪器设备共享服务平台')
            #仪器id
            result = urlparse.urlparse(href)
            params = urlparse.parse_qs(result.query, True)  
            equipment['source_id'] = params['id'][0]

            innerHtml = urlopen(href)
            innerDoc = BeautifulSoup(innerHtml.read(), "html5lib")
            container = innerDoc.find('table', {"bgcolor": "#B0C4DE"})

            model = container.find('td', string = '仪器型号')
            equipment['model'] = model.find_next_sibling().string

            manu_name = container.find('td', string = '仪器厂商')
            equipment['manu_name'] = manu_name.find_next_sibling().string

            price = container.find('td', string = '仪器原值')
            equipment['price'] = str(price.find_next_sibling().string).replace('万元', '0000')

            purchased_date = container.find('td', string = '购买时间') 
            equipment['purchased_date'] = purchased_date.find_next_sibling().string

            application = container.find('td', string = '服务领域') 
            equipment['application'] = application.find_next_sibling().string

            institute = container.find('td', string = '所在单位')
            equipment['institute'] = institute.find_next_sibling().string

            tech_specs = container.find('td', string = '技术指标')
            equipment['tech_specs'] = tech_specs.find_next_sibling().string

            features = container.find('td', string = '仪器用途')
            equipment['features'] = features.find_next_sibling().string

            equipment['share'] = 1

            yiqikong.call("YiQiKong/Directory/Add", equipment)
            time.sleep(0.2)
        except:
            file.write('page: ' + str(j) + ' link: ' + link['href'])
            file.write('\n')
            continue
    j += 1
file.close()
