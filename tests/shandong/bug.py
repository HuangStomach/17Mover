# -*- coding: UTF-8 -*-
import time
import pyjsonrpc
from urllib import urlopen
from bs4 import BeautifulSoup

def iconv(str, code = 'utf8'):
    if (str is None or len(str) == 0):
        return ''
    else:
        return str.encode(code)

i = 9328
j = 932
file = open('retry.txt', 'a')
base = "http://www.sdkxyq.com"

while 1 == 1:
    html = urlopen(base + "/Ins/IndexPanel?pageindex=" + str(j))
    doc = BeautifulSoup(html.read(), "html5lib")

    yiqikong = pyjsonrpc.HttpClient(
        url = "http://directory.17kong.com/api"
    )
    
    links = doc.findAll("a", {"class": "check_detail"})
    
    if (len(links) == 0):
        break
    
    for link in links:
        try:
            equipment = {}
            href = base + link['href']
            #仪器名称
            equipment["name"] = iconv(link.find_previous_sibling("h1").a.string)
            print equipment["name"]

            innerHtml = urlopen(href)
            innerDoc = BeautifulSoup(innerHtml.read(), "html5lib")
            container = innerDoc.find('div', {"class": "equdetail_page"})

            #仪器图片
            equipment['icon'] = base + container.find('img', {"id": "Ins_Img"})['src']

            #所属单位
            equipment['institute'] = [iconv(container.find('span', {"id": "UnitDept"}).string)]
            #仪器来源
            equipment['source_name'] = iconv(container.find('span', {"id": "Company_Name"}).string)

            ttl = iconv(container.find('div', {"class": "equdetail_page_part"}).string).strip()
            ttls = ttl.split()

            for item in ttls:
                if (item.find("仪器编号") >= 0):
                    start = item.find("：") + 3
                    end = len(item)
                    equipment['ref_no'] = item[start:end]
                    equipment['source_id'] = i

            #仪器型号
            equipment['model'] = iconv(container.find('span', {"id": "Ins_Version"}).string)
            #仪器价格
            price = iconv(container.find('span', {"id": "Ins_OriginalValue"}).string)
            equipment['price'] = int(float(price)) * 1000
            #制造厂商
            equipment['manu_name'] = iconv(container.find('span', {"id": "Ins_Producer"}).string)
            #出厂日期
            equipment['manu_date'] = iconv(container.find('span', {"id": "ProductTime"}).string)
            #购置日期
            equipment['purchased_date'] = iconv(container.find('span', {"id": "ProductTime"}).string)
            #技术指标
            equipment['tech_specs'] = iconv(container.find('span', {"id": "TechIssues"}).string)
            #功能特色
            equipment['features'] = iconv(container.find('span', {"id": "Ins_Function"}).string)
            #附件配置
            equipment['accessories'] = iconv(container.find('span', {"id": "MainAccessories"}).string) + iconv(container.find('span', {"id": "MainAccessories2"}).string)
            #主要领域
            science = iconv(container.find('span', {"id": "Ins_Subject_Id"}).string)
            service = iconv(container.find('span', {"id": "ServiceField2"}).string)
            equipment['application'] = (','.join([science, service])).strip(',')
            #联系人员
            equipment['contact_name'] = iconv(container.find('span', {"id": "Company_Contact_Name"}).string)
            equipment['contact_phone'] = iconv(container.find('span', {"id": "Company_Contact_Tel"}).string)
            equipment['contact_email'] = iconv(container.find('span', {"id": "Company_Contact_Email"}).string)
            #放置地点
            equipment['location'] = iconv(container.find('span', {"id": "Company_Address"}).string)

            equipment['share'] = 1;

            yiqikong.call("YiQiKong/Directory/Add", equipment)
            i += 1
            time.sleep(0.2)
        except:
            file.write(link['href'])
            file.write('\n')
            continue
    j += 1;
file.close()
