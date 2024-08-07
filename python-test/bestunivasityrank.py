#爬取最好大学排名
import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
def fillUnivList(ulist,html):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children:
            if isinstance(tr, bs4.element.Tag):
                tds = tr('td')
                uname=tds[1].find('div', attrs={'class':'link-container'}).text.strip()
            ulist.append([tds[0].string.strip(), uname, tds[4].text.strip()])
     
def printUnivList(ulist, num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format("排名", "学校", "分数",chr(12288)))
    for i in range(num):
        u=ulist[i]
        print(tplt.format(u[0], u[1], u[2],chr(12288)))
    
def main():
    url = 'https://www.shanghairanking.cn/rankings/bcur/202411'
    uinfo = []
    html = getHTMLText(url)
    fillUnivList(uinfo,html)
    printUnivList(uinfo, len(uinfo))
main()