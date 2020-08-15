import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading
class Procuder(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Procuder,self).__init__(*args,**kwargs)
        self.page_queue=page_queue
        self.img_queue=img_queue
    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url=self.page_queue.get()
            self.parse_page(url)

    def parse_page(self,url):
        response=requests.get(url,headers=self.headers)
        text=response.text
        #使用entree 去解析数据
        html=etree.HTML(text)
        imgs=html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
        # print(etree.tostring(img))#etree.tostring(img)
        # 将其转换为字符
        for img in imgs:
            img_url=img.get("data-original")
            alt=img.get("alt")
            alt=re.sub(r"[\?？\.。！!\*]","",alt)
            suffix=os.path.splitext(img_url)[1]
            filename=alt+suffix
            self.img_queue.put((img_url,filename))

class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue=page_queue
        self.img_queue=img_queue
    def run(self):
        while True:
            if self.page_queue.empty() and self.img_queue.empty():
                break
            img_url,filename=self.img_queue.get()
            request.urlretrieve(img_url,"斗图照片/"+filename)
            print(filename+"下载完成！")

def main():
    page_queue=Queue(100)
    img_queue=Queue(1000)
    for x in range(1,100):#根据网站的页数选定合适的爬取
        url = "https://www.doutula.com/photo/list/?page={}".format(x)
        page_queue.put(url)
    for x in range(5):
        t=Procuder(page_queue,img_queue)
        t.start()

    for x in range(5):
        t=Consumer(page_queue,img_queue)
        t.start()

if __name__ == '__main__':
    main()