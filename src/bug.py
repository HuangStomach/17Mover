from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.sdkxyq.com/Ins/IndexPanel?pageindex=1")
doc = BeautifulSoup(html.read())

links = doc.findAll("a", {"class": "check_detail"})
for link in links:
    print(link['href'])
