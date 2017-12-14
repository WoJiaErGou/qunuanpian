import scrapy
from scrapy import Selector
import requests
import re
import pandas as pd
from requests import Session,adapters
from bs4 import BeautifulSoup
import json
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from qunuanpian_sn.items import QunuanpianSnItem
class QunuanQiSpider(scrapy.Spider):
    name = 'qnp_sn'
    start_urls=['https://list.suning.com/0-20370-0.html']
    def start_requests(self):
        '''
        后续补充
        '''
        database=pd.read_csv('luanxu.csv')
        url_list=list(database['url'])
        ProgramStarttime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item=QunuanpianSnItem(ProgramStarttime=ProgramStarttime)
        # url='https://product.suning.com/0000000000/694729819.html'
        for each in url_list:
        # for i in range(0,200):
        #     each=url_list[i]
            yield scrapy.Request(url=each,callback=self.parse,dont_filter=False,meta={'item':item})
    def parse(self, response):
        if len(response.text) < 70000:
            yield scrapy.Request(url=response.request.url,callback=self.parse,dont_filter=True,meta=response.meta)
            return None
        item=response.meta['item']
        response_text=response.text
        #商品链接
        product_url=response.request.url
        #商品ID
        ProductID=product_url.split('/')[-1].split('.')[0]
        #商品链接urlID
        urlID=product_url.split('/')[-2]
        #店铺名称
        try:
            shop_name=re.findall('shopName":"(.*?)"',response_text)[0]
        except:
            try:
                shop_name=re.findall('"curShopName":.*?>(.*?)</a>"',response_text)[0]
            except:
                try:
                    shop_name=response.xpath(".//div[@class='si-intro-list']/dl[1]/dd/a/text()").extract()[0]
                except:
                    shop_name=None
        #商品名称
        try:
            p_Name=response.xpath(".//div[@class='imgzoom-main']/a[@id='bigImg']/img/@alt").extract()[0]
        except:
            try:
                p_Name=re.findall('"itemDisplayName":"(.*?)"',response_text)[0]
            except:
                p_Name=None
        # 品牌
        try:
            brand = Selector(response).re('"brandName":"(.*?)"')[0]
        except:
            try:
                brand = Selector(response).re('品牌</span>.*?target="_blank">美的(Midea)</a>')[0]
            except:
                try:
                    brand = re.findall('"brandName":"(.*?)"', response_text)[0]
                except:
                    brand = None
        # 去掉品牌括号内容
        if brand:
            brand = brand[:0] + re.sub(r'（.*?）', '', brand)
            brand = brand[:0] + re.sub(r'\(.*?\)', '', brand)
        #型号
        try:
            X_name=re.findall('型号</span> </div> </td> <td class="val">(.*?)</td>',response_text)[0]
        except:
            try:
                X_name=Selector(response).re('型号</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                X_name=None
        if X_name:
            if brand:
                if brand in X_name:
                    X_name=X_name[:0]+re.sub(brand,'',X_name)
            X_name = X_name[:0] + re.sub(r'（.*?）', '', X_name)
            X_name = X_name[:0] + re.sub(r'\(.*?\)', '', X_name)
        #类别
        try:
            X_type = Selector(response).re('类别：(.*?)</li>')[0]
        except:
            try:
                X_type = Selector(response).re('类别</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    X_type = re.findall('类别：(.*?)</li>', response_text)[0]
                except:
                    try:
                        X_type=re.findall('类别</span> </div> </td> <td class="val">(.*?)</td>',response_text)[0]
                    except:
                        X_type = None
        #颜色
        try:
            color = Selector(response).re('颜色：(.*?)</li>')[0]
        except:
            try:
                color = Selector(response).re('颜色</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    color = re.findall('颜色：(.*?)</li>', response_text)[0]
                except:
                    try:
                        color=re.findall('颜色</span> </div> </td> <td class="val">(.*?)</td>',response_text)[0]
                    except:
                        color = None
        #适用面积
        try:
            adapt_area = Selector(response).re('适用面积：(.*?)</li>')[0]
        except:
            try:
                adapt_area = Selector(response).re('适用面积</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    adapt_area = re.findall('适用面积：(.*?)</li>', response_text)[0]
                except:
                    try:
                        adapt_area=re.findall('适用面积</span> </div> </td> <td class="val">(.*?)</td>',response_text)[0]
                    except:
                        adapt_area = None
        # 放置方式
        try:
            placement = Selector(response).re('放置方式：(.*?)</li>')[0]
        except:
            try:
                placement = Selector(response).re('放置方式</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    placement = re.findall('放置方式：(.*?)</li>', response_text)[0]
                except:
                    try:
                        placement = re.findall('放置方式</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        placement = None
        # 加热方式
        try:
            heat = Selector(response).re('加热方式：(.*?)</li>')[0]
        except:
            try:
                heat = Selector(response).re('加热方式</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    heat = re.findall('加热方式：(.*?)</li>', response_text)[0]
                except:
                    try:
                        heat = re.findall('加热方式</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        heat = None
        # 控制方式
        try:
            control = Selector(response).re('控制方式：(.*?)</li>')[0]
        except:
            try:
                control = Selector(response).re('控制方式</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    control = re.findall('控制方式：(.*?)</li>', response_text)[0]
                except:
                    try:
                        control = re.findall('控制方式</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        control = None
        # 加热片数量
        try:
            brand_num = Selector(response).re('加热片数量：(.*?)</li>')[0]
        except:
            try:
                brand_num = Selector(response).re('加热片数量</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    brand_num = re.findall('加热片数量：(.*?)</li>', response_text)[0]
                except:
                    try:
                        brand_num = re.findall('加热片数量</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        brand_num = None
        # 档位
        try:
            gear = Selector(response).re('档位：(.*?)</li>')[0]
        except:
            try:
                gear = Selector(response).re('档位</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    gear = re.findall('档位：(.*?)</li>', response_text)[0]
                except:
                    try:
                        gear = re.findall('档位</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        gear = None
        # 产品尺寸
        try:
            size = Selector(response).re(r'产品尺寸\(高\*宽\*深</span> </div> </td> <td class="val">(.*?)</td>')[0]
        except:
            try:
                size = re.findall(r'产品尺寸\(高\*宽\*深</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
            except:
                try:
                    size = re.findall(r'产品尺寸\(高\*宽\*深</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                except:
                    size = None
        # 倾倒断电
        try:
            dump_off = Selector(response).re('倾倒断电：(.*?)</li>')[0]
        except:
            try:
                dump_off = Selector(response).re('倾倒断电</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    dump_off = re.findall('倾倒断电：(.*?)</li>', response_text)[0]
                except:
                    try:
                        dump_off = re.findall('倾倒断电</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        dump_off = None
        # 定时功能
        try:
            time = Selector(response).re('定时功能：(.*?)</li>')[0]
        except:
            try:
                time = Selector(response).re('定时功能</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    time = re.findall('定时功能：(.*?)</li>', response_text)[0]
                except:
                    try:
                        time = re.findall('定时功能</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        time = None
        # 恒温功能
        try:
            constant_temp = Selector(response).re('恒温功能：(.*?)</li>')[0]
        except:
            try:
                constant_temp = Selector(response).re('恒温功能</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    constant_temp = re.findall('恒温功能：(.*?)</li>', response_text)[0]
                except:
                    try:
                        constant_temp = re.findall('恒温功能</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        constant_temp = None
        #遥控功能
        try:
            telecontrol = Selector(response).re('遥控功能：(.*?)</li>')[0]
        except:
            try:
                telecontrol = Selector(response).re('遥控功能</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    telecontrol = re.findall('遥控功能：(.*?)</li>', response_text)[0]
                except:
                    try:
                        telecontrol = re.findall('遥控功能</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        telecontrol = None
        #防水功能
        try:
            waterproof = Selector(response).re('防水功能：(.*?)</li>')[0]
        except:
            try:
                waterproof = Selector(response).re('防水功能</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    waterproof = re.findall('防水功能：(.*?)</li>', response_text)[0]
                except:
                    try:
                        waterproof = re.findall('防水功能</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        waterproof = None
        if waterproof == None:
            try:
                may_fun = re.findall('支持功能：(.*?)</li>', response_text)[0]
                if '防水' in may_fun:
                    waterproof = '支持'
            except:
                waterproof = None
        # print(waterproof)
        #摇头功能
        try:
            shake = Selector(response).re('摇头功能：(.*?)</li>')[0]
        except:
            try:
                shake = Selector(response).re('摇头功能</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    shake = re.findall('摇头功能：(.*?)</li>', response_text)[0]
                except:
                    try:
                        shake = re.findall('摇头功能</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        shake = None
        #浴居两用
        try:
            bath_house = Selector(response).re('浴居两用：(.*?)</li>')[0]
        except:
            try:
                bath_house = Selector(response).re('浴居两用</span> </div> </td> <td class="val">(.*?)</td>')[0]
            except:
                try:
                    bath_house = re.findall('浴居两用：(.*?)</li>', response_text)[0]
                except:
                    try:
                        bath_house = re.findall('浴居两用</span> </div> </td> <td class="val">(.*?)</td>', response_text)[0]
                    except:
                        bath_house = None
        # 核心参数
        type = '"'
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            ul = soup.find('ul', attrs={'class': 'cnt clearfix'})
            li = ul.find_all('li')
            for i in range(len(li)):
                type = type[:] + li[i].text
                if i < len(li) - 1:
                    type = type[:] + ' '
                if i == len(li) - 1:
                    type = type[:] + '"'
        except:
            try:  # 部分核心参数格式更改
                div = soup.find('div', class_='prod-detail-container')
                ul = div.find('ul', attrs={'class': 'clearfix'})
                li = ul.find_all('li')
                for each in li:
                    li_li = each.find_all('li')
                    for i in range(len(li_li)):
                        type = type[:] + li_li[i].text
                        if i < len(li_li) - 1:
                            type = type[:] + ' '
                        if i == len(li_li) - 1:
                            type = type[:] + '"'
            except:
                type = None
        if type:
            if len(type) < 2:
                type = None
        if type == None:
            try:
                parameter_id = Selector(response).re('"mainPartNumber":"(.*?)"')[0]
            except:
                try:
                    parameter_id = re.findall('"mainPartNumber":"(.*?)"', response_text)[0]
                except:
                    parameter_id = None
                    type = None
            if parameter_id:
                try:
                    parameter_id = Selector(response).re('"mainPartNumber":"(.*?)"')[0]
                    parameter_url = 'https://product.suning.com/pds-web/ajax/itemParameter_%s_R0105002_10051.html' % parameter_id
                    para_response = requests.get(parameter_url).text
                    sleep(1)
                    eles = re.findall('"snparameterdesc":"(.*?)"', para_response)
                    souls = re.findall('"snparameterVal":"(.*?)"', para_response)
                    try:
                        type = '"'
                        for i in range(len(eles)):
                            type = type[:] + eles[i] + ':' + souls[i]
                            if i < len(eles) - 1:
                                type = type[:] + ' '
                            if i == len(eles) - 1:
                                type = type[:] + '"'
                            if len(type) < 2:
                                type = None
                    except:
                        type = None
                    #品牌
                    if brand == None:
                        try:
                            brand = re.findall('"snparameterdesc":"品牌","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            brand = None
                    #型号
                    if X_name == None:
                        try:
                            X_name = re.findall('"snparameterdesc":"型号","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            X_name = None
                    if X_name:
                        if brand:
                            if brand in X_name:
                                X_name = X_name[:0] + re.sub(brand, '', X_name)
                        X_name = X_name[:0] + re.sub(r'（.*?）', '', X_name)
                        X_name = X_name[:0] + re.sub(r'\(.*?\)', '', X_name)
                    #类别
                    if X_type == None:
                        try:
                            X_type = re.findall('"snparameterdesc":"类别","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            X_type = None
                    #颜色
                    if color == None:
                        try:
                            color = re.findall('"snparameterdesc":"颜色","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            color = None
                    #适用面积
                    if adapt_area == None:
                        try:
                            adapt_area = re.findall('"snparameterdesc":"适用面积","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            adapt_area = None
                    #放置方式
                    if placement == None:
                        try:
                            placement = re.findall('"snparameterdesc":"放置方式","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            placement = None
                    #加热方式
                    if heat == None:
                        try:
                            heat = re.findall('"snparameterdesc":"加热方式","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            heat = None
                    #控制方式
                    if control == None:
                        try:
                            control = re.findall('"snparameterdesc":"控制方式","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            control = None
                    #加热片数量
                    if brand_num == None:
                        try:
                            brand_num = re.findall('"snparameterdesc":"加热片数量","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            brand_num = None
                    #档位
                    if gear == None:
                        try:
                            gear = re.findall('"snparameterdesc":"档位","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            gear = None
                    #产品尺寸
                    if size == None:
                        try:
                            size = re.findall('"snparameterdesc":"产品尺寸","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            size = None
                    #倾倒断电
                    if dump_off == None:
                        try:
                            dump_off = re.findall('"snparameterdesc":"倾倒断电","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            dump_off = None
                    #定时功能
                    if time == None:
                        try:
                            time = re.findall('"snparameterdesc":"定时功能","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            time = None
                    #恒温功能
                    if constant_temp == None:
                        try:
                            constant_temp = re.findall('"snparameterdesc":"恒温功能","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            constant_temp = None
                    # 遥控功能
                    if telecontrol == None:
                        try:
                            telecontrol = re.findall('"snparameterdesc":"遥控功能","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            telecontrol = None
                    #防水功能
                    if waterproof == None:
                        try:
                            waterproof = re.findall('"snparameterdesc":"防水功能","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            waterproof = None
                    #摇头功能
                    if shake == None:
                        try:
                            shake = re.findall('"snparameterdesc":"摇头功能","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            shake = None
                    #浴居两用
                    if bath_house == None:
                        try:
                            bath_house = re.findall('"snparameterdesc":"浴居两用","snparameterVal":"(.*?)"', para_response)[0]
                        except:
                            bath_house = None
                except:
                    pass
        # 获取相关请求url
        keyword_url = 'https://review.suning.com/ajax/getreview_labels/general-000000000' + ProductID + '-' + urlID + '-----commodityrLabels.htm'
        comment_url = 'https://review.suning.com/ajax/review_satisfy/general-000000000' + ProductID + '-' + urlID + '-----satisfy.htm'
        price_url = 'https://pas.suning.com/nspcsale_0_000000000' + ProductID + '_000000000' + ProductID + '_' + urlID + '_10_010_0100101_20268_1000000_9017_10106_Z001.html'
        # 获取印象关键字
        try:
            keyword_response = requests.get(keyword_url).text
            keyword_text = json.loads(re.findall(r'\((.*?)\)', keyword_response)[0])
            keyword_list = keyword_text.get('commodityLabelCountList')
            key_str = '"'
            keyword = []
            for i in range(len(keyword_list)):
                key_str = key_str[:] + keyword_list[i].get('labelName')
                if i < len(keyword_list) - 1:
                    key_str = key_str[:] + ' '
                if i == len(keyword_list) - 1:
                    key_str = key_str[:] + '"'
            keyword.append(key_str)
        except:
            keyword = None
        # 获取评价信息
        try:
            comment_response = requests.get(comment_url).text
            comment_text = json.loads(re.findall(r'\((.*?)\)', comment_response)[0])
            comment_list = comment_text.get('reviewCounts')[0]
            # 差评
            PoorCount = comment_list.get('oneStarCount')
            twoStarCount = comment_list.get('twoStarCount')
            threeStarCount = comment_list.get('threeStarCount')
            fourStarCount = comment_list.get('fourStarCount')
            fiveStarCount = comment_list.get('fiveStarCount')
            # 评论数量
            CommentCount = comment_list.get('totalCount')
            # 好评
            GoodCount = fourStarCount + fiveStarCount
            # 中评
            GeneralCount = twoStarCount + threeStarCount
            # 好评度
            # 得到百分比取整函数
            if CommentCount != 0:
                goodpercent = round(GoodCount / CommentCount * 100)
                generalpercent = round(GeneralCount / CommentCount * 100)
                poorpercent = round(PoorCount / CommentCount * 100)
                commentlist = [GoodCount, GeneralCount, PoorCount]
                percent_list = [goodpercent, generalpercent, poorpercent]
                # 对不满百分之一的判定
                for i in range(len(percent_list)):
                    if percent_list[i] == 0 and commentlist[i] != 0 and CommentCount != 0:
                        percent_list[i] = 1
                nomaxpercent = 0  # 定义为累计不是最大百分比数值
                # 好评度计算url='http://res.suning.cn/project/review/js/reviewAll.js?v=20170823001'
                if CommentCount != 0:
                    maxpercent = max(goodpercent, generalpercent, poorpercent)
                    for each in percent_list:
                        if maxpercent != each:
                            nomaxpercent += each
                    GoodRateShow = 100 - nomaxpercent
                else:
                    GoodRateShow = 100
            else:
                PoorCount = 0
                CommentCount = 0
                GoodCount = 0
                GeneralCount = 0
                GoodRateShow = 100
        except:
            PoorCount = 0
            CommentCount = 0
            GoodCount = 0
            GeneralCount = 0
            GoodRateShow = 100
        # 有关价格
        try:
            price_response = requests.get(price_url).text
        except requests.RequestException as e:
            # print(e)
            sleep(2)
            s = requests.session()
            s.keep_alive = False
            s.mount('https://', HTTPAdapter(max_retries=5))
            price_response = s.get(price_url).text
        if len(price_response) > 900:
            try:
                price = re.findall('"refPrice":"(.*?)"', price_response)[0]
                PreferentialPrice = re.findall('"promotionPrice":"(.*?)"', price_response)[0]
                if len(price) < 1:
                    price = re.findall('"netPrice":"(.*?)"', price_response)[0]
                if price:
                    if float(price) < float(PreferentialPrice):
                        tt = price
                        price = PreferentialPrice
                        PreferentialPrice = tt
            except:
                price = None
                PreferentialPrice = None
        else:
            sleep(3)
            price_response = requests.get(price_url).text
            if len(price_response) > 900:
                try:
                    price = re.findall('"refPrice":"(.*?)"', price_response)[0]
                    PreferentialPrice = re.findall('"promotionPrice":"(.*?)"', price_response)[0]
                    if len(price) < 1:
                        price = re.findall('"netPrice":"(.*?)"', price_response)[0]
                    if price:
                        if float(price) < float(PreferentialPrice):
                            tt = price
                            price = PreferentialPrice
                            PreferentialPrice = tt
                except:
                    price = None
                    PreferentialPrice = None
            else:
                # 作出失败判断并将url归入重试
                price_response = self.retry_price(price_url)
                if len(price_response) > 500:
                    try:
                        price = re.findall('"refPrice":"(.*?)"', price_response)[0]
                        PreferentialPrice = re.findall('"promotionPrice":"(.*?)"', price_response)[0]
                        if len(price) < 1:
                            price = re.findall('"netPrice":"(.*?)"', price_response)[0]
                        if price:
                            if float(price) < float(PreferentialPrice):
                                tt = price
                                price = PreferentialPrice
                                PreferentialPrice = tt
                    except:
                        price = None
                        PreferentialPrice = None
                else:
                    PreferentialPrice = None
                    price = None
        '''
        # 默认参数，修正数据格式
        '''
        #产品尺寸
        if size:
            size=re.sub(r'[\u4e00-\u9fa5]+','',size)
        # 来源
        source='苏宁'
        #修正数据
        if type==None and brand==None and X_name==None:
            print('一条数据被过滤！')
            yield None
        else:
            item['ProductID']=ProductID
            item['X_name'] = X_name
            item['type'] = type
            item['X_type'] = X_type
            item['price'] = price
            item['PreferentialPrice'] = PreferentialPrice
            item['brand'] = brand
            item['keyword'] = keyword
            item['PoorCount'] = PoorCount
            item['CommentCount'] = CommentCount
            item['GoodCount'] = GoodCount
            item['GeneralCount'] = GeneralCount
            item['GoodRateShow'] = GoodRateShow
            item['shop_name'] = shop_name
            item['product_url'] = product_url
            item['color'] = color
            item['adapt_area'] = adapt_area
            item['placement'] = placement
            item['heat'] = heat
            item['control'] = control
            item['brand_num'] = brand_num
            item['gear'] = gear
            item['size'] = size
            item['dump_off'] = dump_off
            item['time'] = time
            item['constant_temp'] = constant_temp
            item['telecontrol'] = telecontrol
            item['waterproof'] = waterproof
            item['shake'] = shake
            item['bath_house'] = bath_house
            item['source'] = source
            item['p_Name']=p_Name
            yield item


    def retry_price(self,price_url):
        price_response_may = requests.get(price_url)
        time.sleep(5)
        price_response=price_response_may.text
        return price_response