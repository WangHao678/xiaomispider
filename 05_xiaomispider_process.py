'''
运用多进程爬取小米应用商城应用信息,并保存为csv文件
'''
import requests
#队列模块必须使用 multiprocessing中的Queue,支持进程间通信
from multiprocessing import Process,Lock,Queue
import json
from queue import Queue
import time
import random
from fake_useragent import UserAgent
from lxml import etree
import csv

class XiaomiSpider(object):
    def __init__(self):
        self.url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId={}&pageSize=30'
        self.q = Queue()
        self.i = 0
        #创建互斥锁
        self.lock = Lock()
        self.f = open('小米.csv','a',newline='')
        self.writer = csv.writer(self.f)

    #功能函数:获取响应内容
    def get_html(self,url):
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url,headers=headers).text
        return html

    #获取所有类别的ID
    def get_id(self):
        url = 'http://app.mi.com/'
        html = self.get_html(url)
        p = etree.HTML(html)
        li_list = p.xpath('//div[@class="sidebar"]/div[2]/ul[1]/li')
        for li in li_list:
            id = li.xpath('./a/@href')[0].split('/')[-1] #href="/category/15"
            #type_name = li.xpath('./a/text()')[0]
            self.url_in(id)

    #url入队列
    def url_in(self,id):
        #获取指定应用类别的总页数
        total = self.get_total(id)
        for page in range(0,total):
            url = self.url.format(page,id)
            self.q.put(url)

    #获取总页数
    def get_total(self,id):
        url = self.url.format(0,id)
        html = json.loads(self.get_html(url))
        #count:为应用的数量
        count = int(html['count'])
        if count % 30 == 0:
            total = count//30
        else:
            total = count // 30 + 1
        return total

    #线程时间函数: 请求+解析+保持
    def parse_html(self):
        while True:
            if not self.q.empty():
                url = self.q.get()
                html = json.loads(self.get_html(url))
                item = {}
                app_list = []
                for app in html['data']:
                    item['name'] = app['displayName']
                    item['type'] = app['level1CategoryName']
                    item['link'] = app['packageName']
                    app_list.append((item['name'],item['type'],item['link']))
                    print(item)
                #写文件需要加锁
                self.lock.acquire()
                self.writer.writerows(app_list)
                self.lock.release()
                time.sleep(random.uniform(0,1))
            else:
                break

    def run(self):
        self.get_id()
        t_list = []
        for i in range(1):
            t = Process(target=self.parse_html)
            t_list.append(t)
            t.start()

        for j in t_list:
            j.join()

        #最终关闭文件
        self.f.close()

if __name__ == '__main__':
    begin = time.time()
    spider = XiaomiSpider()
    spider.run()
    end = time.time()
    print('执行时间:%.2f' %(end-begin))




















