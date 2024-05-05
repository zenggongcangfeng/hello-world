import requests
import re

def get_one_page(url):
    # 构造请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    
    
    # 发送GET请求
    response = requests.get(url, headers=headers)
    
    #判断请求是否正常
    if response.status_code == 200:
        return response.text
    return None

def parse_one_page(html):
    # 解析网页内容
    # ...
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    print(items)

if __name__ == '__main__':
    url = 'https://www.maoyan.com/board/4'
    html = get_one_page(url)
    parse_one_page(html)
    

   