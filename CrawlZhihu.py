import re
import json
import requests
from lxml import etree
import random
import time
import numpy as np
import jsonpath
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium import webdriver

# 读取代理域名
f = open('./代理域名.txt', )
a = []
for i in f.readlines():
    a.append(i.strip('\n'))
f.close()


class CrawlZhihuHostList():
    def __init__(self):
        self.dict1 = {}
        self.n = -1
        self.hotLink_list = []
        proxy_arr = ['http://' + random.choice(a), 'https://' + random.choice(a)]
        proxies = random.choice(proxy_arr)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")
        options.add_argument(proxies) #避免频繁使用一个IP地址爬取被检测出来
        s = Service(r"./chromedriver")
        self.web = webdriver.Chrome(service=s, options=options)
        self.web.get('https://www.zhihu.com/hot')
        self.web.delete_all_cookies()
        time.sleep(1)
        self.web.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[3]/span/button[2]').click()
        self.web.switch_to.window(self.web.window_handles[-1])
        self.web.switch_to.frame('ptlogin_iframe')
        print("QQ登录：", self.web.current_url)
        time.sleep(3)
        self.web.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[8]/div/a').click()
        self.web.back()
        self.web.switch_to.window(self.web.window_handles[0])
        time.sleep(5)
        html = etree.HTML(self.web.page_source)
        urls = html.xpath('//*[@id="TopstoryContent"]/div/div/div[1]/section/div[2]/a/@href')
        print('热榜数量', len(urls))
        self.CrawHotList(urls)
        time.sleep(50)

    def readExistUrl(self):
        hotLink = pd.read_csv('./事件顺序.csv', usecols=[2])
        hotLink_list = np.array(hotLink).tolist()
        return hotLink_list

    def DuplicateRemoval(self, url):
        count = self.hotLink_list.count([url])
        return count

    def CrawHotOne(self, url):
        # 1.热搜去重
        count = self.DuplicateRemoval(url)
        if (count > 0):
            return
        # 2.爬取当前事件
        headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'}
        r = requests.get(url, headers=headers)
        try:
            title = jsonpath.jsonpath(
                json.loads(re.findall(r'<script id="js-initialData" type="text/json">(.*?)</script>', r.text)[0]),
                '$..entities.questions..title')
        except:
            title = ''
        if title:
            title = title[0]
        try:
            content = ''.join(re.findall(r'<p>(.*?)</p>', jsonpath.jsonpath(
                json.loads(re.findall(r'<script id="js-initialData" type="text/json">(.*?)</script>', r.text)[0]),
                '$..entities.questions..detail')[0]))
            if content == '':
                content = jsonpath.jsonpath(
                    json.loads(re.findall(r'<script id="js-initialData" type="text/json">(.*?)</script>', r.text)[0]),
                    '$..entities.questions..excerpt')[0]
        except:
            content = ''
        # 注意这里的 id 要取 url 的最后面的数字
        url_split = url.split('/')
        id = url_split[len(url_split) - 1]
        self.n += 1
        self.dict1[self.n] = {}
        self.dict1[self.n]['hotLink'] = r.url
        self.dict1[self.n]['hotId'] = id
        self.dict1[self.n]['hotTitle'] = title
        self.dict1[self.n]['hotContent'] = content
        print("链接:", r.url, "ID:", id, "标题:", title, "内容:", content)
        if jsonpath.jsonpath(
                json.loads(re.findall(r'<script id="js-initialData" type="text/json">(.*?)</script>', r.text)[0]),
                '$..events'):
            cols = jsonpath.jsonpath(
                json.loads(re.findall(r'<script id="js-initialData" type="text/json">(.*?)</script>', r.text)[0]),
                '$..events')[0]
            hotTime = str(datetime.fromtimestamp(cols[0]['created']))
            prior_node_id = cols[1]['id']
            self.dict1[self.n]['hotTime'] = hotTime
            self.dict1[self.n]['hotPriorId'] = prior_node_id
            print("时间:", hotTime, "前事件ID:", prior_node_id)
            # 3.爬取前馈事件
            for i in range(1, len(cols)):
                url1 = cols[i]['url']
                id1 = cols[i]['id']
                # 3.1 热搜去重
                count1 = self.DuplicateRemoval(url1)
                if (count1 > 0):
                    return
                # 3.2 爬取事件
                r1 = requests.get(url1, headers = headers)
                time.sleep(1)
                try:
                    title1 = jsonpath.jsonpath(json.loads(
                        re.findall(r'<script id="js-initialData" type="text/json">(.*?)</script>', r1.text)[
                            0]), '$..entities.questions..title')[0]
                except:
                    title1 = ''
                try:
                    content1 = ''.join(re.findall(r'<p>(.*?)</p>', jsonpath.jsonpath(json.loads(
                        re.findall(r'<script id="js-initialData" type="text/json">(.*?)</script>', r1.text)[0]),
                        '$..entities.questions..detail')[
                        0]))
                    if content1 == '':
                        content1 = jsonpath.jsonpath(json.loads(
                            re.findall(r'<script id="js-initialData" type="text/json">(.*?)</script>', r1.text)[
                                0]), '$..entities.questions..excerpt')[0]
                except:
                    content1 = ''
                self.n += 1
                self.dict1[self.n] = {}
                self.dict1[self.n]['hotLink'] = url1
                self.dict1[self.n]['hotId'] = id1
                self.dict1[self.n]['hotTitle'] = title1
                self.dict1[self.n]['hotContent'] = content1
                print("链接:", url1, "ID:", id1, "标题:", title1, "内容:", content1)
                hotTime1 = str(datetime.fromtimestamp(cols[i]['created']))
                prior_node_id1 = cols[i + 1]['id'] if i < len(cols) - 1 else ''
                self.dict1[self.n]['hotTime'] = hotTime1
                self.dict1[self.n]['hotPriorId'] = prior_node_id1
                print("时间:", hotTime1, "前事件ID:", prior_node_id1)
        else:
            self.dict1[self.n]['hotPriorId'] = ''
            self.dict1[self.n]['hotTime'] = ''

    def CrawHotList(self, urls):
        # 1.读取已有Url列表
        self.hotLink_list = self.readExistUrl()
        # 2.爬取知乎热榜
        num = 1
        for url in urls:
            print("-" * 50, num, "-" * 50)
            self.CrawHotOne(url)
            num += 1
        # 3.保存热榜信息
        rows = []
        for value in self.dict1.values():
            rows.append(value)
        df = pd.DataFrame(rows)
        output_columns = ["hotId", "hotPriorId", "hotTime", "hotLink", "hotTitle", "hotContent"]
        try:
            df.to_csv("./知乎热榜.csv", mode="a", columns=output_columns, encoding='utf-8', index=False, header=False)
        except:
            print("本次没有新数据")
        # 4.保存事件发展顺序
        order_columns = ["hotId", "hotPriorId", "hotLink"]
        try:
            df.to_csv("./事件顺序.csv", mode="a", columns=order_columns, encoding='utf-8', index=False, header=False)
        except:
            print("本次没有新数据")
        # 5.打日志记录
        df_log = pd.DataFrame({"SavaTime": ["在" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "爬取了" + str(self.n + 1) + "条新数据"]})
        df_log.to_csv("./日志.txt", mode="a", encoding='utf-8', index=False, header=False)
        # 关闭并退出
        print("sucessfully!  Crawled", self.n + 1, "pieces of data.")
        self.web.close()
        exit()


# 执行
CrawlZhihuHostList()