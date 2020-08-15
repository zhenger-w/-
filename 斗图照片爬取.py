import requests
from lxml import etree
from urllib import request
import os
import re

def parse_page(url):
    headers={
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
    }
    response=requests.get(url,headers=headers)
    text=response.text
    #使用entree 去解析数据
    html=etree.HTML(text)
    imgs=html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
    # print(etree.tostring(img))#etree.tostring(img)
    # 将其转换为字符
    for img in imgs:
        url_img=img.get("data-original")
        alt=img.get("alt")
        alt=re.sub(r"[\\\?？\.。！!\*]","",alt)
        suffix=os.path.splitext(url_img)[1]
        file_name=alt+suffix
        request.urlretrieve(url_img,"斗图照片/"+file_name)
        print(file_name+"下载完成！")
num=0
def main():
    global num
    for x in range(1,3):#根据网站的页数选定合适的爬取

        url = "https://www.doutula.com/photo/list/?page={}".format(x)
        num+=1
        print("正在爬取第{}页的斗图".format(num))
        parse_page(url)




if __name__ == '__main__':
    main()