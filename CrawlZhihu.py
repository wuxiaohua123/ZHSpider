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
        cookies = '''_xsrf=bf382fee-3913-4cad-be02-7461b3b5a8b0; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1667176691; d_c0=AJCXCgnyyhWPTp_KT6QvRLH31kKNTDjDNIs=|1667176691; captcha_session_v2=2|1:0|10:1667176691|18:captcha_session_v2|88:TzZtQ2lVQWhLWW93VE5nTS8zcW9TODFBZ3J4eDJIOUJYcFpYcVBNNFR3NGs5d083eE5vN2VHcDhDYVRzL3kzSg==|a158c44606ad09bc4060f94540112a2a9e5ba9165727373314472f341f66c930; SESSIONID=b9DhtLDg0kN5z5qVnsXnGS17i4hXS6Wo4lktSym3KLF; JOID=VVoTBk1SYIhngtOLNVCkn6GLI0UhNV3PDPeay1FjDsJR--f_Z6d_1waG0ow1fqQkNCt5zSDo-Hro6BbSjwGe-_M=; osd=WlkTCkJdY4hrjdyINVyrkKKLL0ouNl3DA_iZy11sAcFR9-jwZKdz2AmF0oA6cackOCR2ziDk93Xr6BrdgAKe9_w=; __snaker__id=vm43QxgfashrxGcd; gdxidpyhxdE=cHd%5CB2tpYImIan7vj%2BcxMql7SEhkWTtT43uee2wRWzgSMAMgdi6v1OzY4%2FJaxRQRxPNJYY4zAxDocjLLuZfWx9dl0IdHwuHKx8vXQW9uL7iZRdxk52lCSaLog2G92u0rEH737lPEQsumv5GkOTBSt8LJh2VrUyfBVVNAQcNc4c%2BlUdnS%3A1667177592267; YD00517437729195%3AWM_NI=zbzKkBJeHASatXyLRIA1tn2yIxaZjWnz8mRJFHkWGoRXPFTVv2kQI5q7eXL0aWo6la9DROAhIMf5p38eZDo218o4voGJOziTAQ3qr3K3buzEktJ%2FuJB%2FJcEyHMwjJDktbDc%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee83d46989e7a196e644a6e78eb6d44f978b9b86c54297a6aab0f243b3e78cd0bb2af0fea7c3b92ababeb6acea4a8abb88a2d26bb888b7add14383efbc8fb1738ba8afbbe95daea6f88ed1428698a5b8c6659288a0a7d75eb6eea5b2cc3fb3e9abb9cf3ca389a1d7ef6bfb9c9eb0c4648b93aad6f339fcbb96a5ee3af3e8a1d5f5658596819bec60838ffd92f13989edae96f94fa9ac86d0f84282f18684c8738c93b98bc950a9acaea5e237e2a3; YD00517437729195%3AWM_TID=v5Tmw5cEcltEVVUVABOFYV2ea8I%2F5Dqt; o_act=login; ref_source=other_https://www.zhihu.com/signin?next=/; expire_in=15552000; q_c1=7351cc2277054142b179c4340d4837b9|1667176702000|1667176702000; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1667176704; z_c0=2|1:0|10:1667176704|4:z_c0|92:Mi4xOW5WR1B3QUFBQUFBa0pjS0NmTEtGUmNBQUFCZ0FsVk5fbVpNWkFBMmt0cENCMnBJNkFDY2dLSWZLX0tRaE9RTE5n|26f732ad1218990b7d5b0b00ef6b330e207c4e06e84cde81efcabb9b36c29e44; NOT_UNREGISTER_WAITING=1; unlock_ticket=ATDYLj5ZuRUXAAAAYAJVTQkgX2PYQsWTeZCvFolUTMdednq3JvTdcw==; KLBRSID=af132c66e9ed2b57686ff5c489976b91|1667176718|1667176690'''
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")
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

    def DuplicateRemoval(self, url):
        hotLink = pd.read_csv('事件顺序.csv', usecols=[2])
        hotLink_list = np.array(hotLink).tolist()
        count = hotLink_list.count([url])
        return count

    def CrawHotOne(self, url):
        # 1.热搜去重
        count = self.DuplicateRemoval(url)
        if (count > 0):
            return
        # 2.爬取当前事件
        self.n += 1
        headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'}
        proxies = {'http': 'http://' + random.choice(a), 'https': 'https://' + random.choice(a)}
        r = requests.get(url, headers=headers)
        htmls = etree.HTML(r.text)
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
            time = str(datetime.fromtimestamp(cols[0]['created']))
            prior_node_id = cols[1]['id']
            self.dict1[self.n]['hotTime'] = time
            self.dict1[self.n]['hotPriorId'] = prior_node_id
            print("时间:", time, "前事件ID:", prior_node_id)
            # 3.爬取前馈事件
            for i in range(1, len(cols)):
                self.n += 1
                self.dict1[self.n] = {}
                url1 = cols[i]['url']
                id1 = cols[i]['id']
                r1 = requests.get(url1, headers = headers)
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
                self.dict1[self.n]['hotLink'] = url1
                self.dict1[self.n]['hotId'] = id1
                self.dict1[self.n]['hotTitle'] = title1
                self.dict1[self.n]['hotContent'] = content1
                print("链接:", url1, "ID:", id1, "标题:", title1, "内容:", content1)
                time1 = str(datetime.fromtimestamp(cols[i]['created']))
                prior_node_id1 = cols[i + 1]['id'] if i < len(cols) - 1 else ''
                self.dict1[self.n]['hotTime'] = time1
                self.dict1[self.n]['hotPriorId'] = prior_node_id1
                print("时间:", time1, "前事件ID:", prior_node_id1)
        else:
            self.dict1[self.n]['hotPriorId'] = ''
            self.dict1[self.n]['hotTime'] = ''

    def CrawHotList(self, urls):
        # 1.爬取知乎热榜
        num = 1
        for url in urls:
            print("-" * 50, num, "-" * 50)
            self.CrawHotOne(url)
            num += 1
        # 2.保存热榜信息
        rows = []
        for value in self.dict1.values():
            rows.append(value)
        df = pd.DataFrame(rows)
        output_columns = ["hotId", "hotPriorId", "hotTime", "hotLink", "hotTitle", "hotContent"]
        try:
            df.to_csv("./知乎热榜.csv", mode="a", columns=output_columns, encoding='utf-8', index=False, header=False)
        except:
            print("本次没有新数据")
        # 3.保存事件发展顺序
        order_columns = ["hotId", "hotPriorId", "hotLink"]
        try:
            df.to_csv("./事件顺序.csv", mode="a", columns=order_columns, encoding='utf-8', index=False, header=False)
        except:
            print("本次没有新数据")
        # 4.打日志记录
        df_log = pd.DataFrame({"SavaTime": ["在" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "爬取了" + str(self.n + 1) + "条新数据"]})
        df_log.to_csv("./日志.txt", mode="a", encoding='utf-8', index=False, header=False)
        # 关闭并退出
        print("sucessfully!  Crawled", self.n + 1, "pieces of data.")
        self.web.close()
        exit()


# 执行
CrawlZhihuHostList()