# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QunuanpianSnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 商品名称
    p_Name = scrapy.Field()
    # 店铺名称
    shop_name = scrapy.Field()
    # 商品ID
    ProductID = scrapy.Field()
    # 原价
    price = scrapy.Field()
    # 折扣价
    PreferentialPrice = scrapy.Field()
    # 评论总数
    CommentCount = scrapy.Field()
    # 好评率
    GoodRateShow = scrapy.Field()
    # 好评
    GoodCount = scrapy.Field()
    # 中评
    GeneralCount = scrapy.Field()
    # 差评
    PoorCount = scrapy.Field()
    # 评论关键词
    keyword = scrapy.Field()
    # 核心参数
    type = scrapy.Field()
    # 品牌
    brand = scrapy.Field()
    # 型号
    X_name = scrapy.Field()
    # 类型
    X_type = scrapy.Field()
    # 颜色
    color = scrapy.Field()
    # 适用面积
    adapt_area = scrapy.Field()
    # 放置方式
    placement = scrapy.Field()
    # 加热方式
    heat = scrapy.Field()
    # 控制方式
    control = scrapy.Field()
    # 加热片数量
    brand_num = scrapy.Field()
    # 档位
    gear = scrapy.Field()
    # 产品尺寸
    size = scrapy.Field()
    # 倾倒断电
    dump_off = scrapy.Field()
    # 定时功能
    time = scrapy.Field()
    # 恒温功能
    constant_temp = scrapy.Field()
    # 遥控功能
    telecontrol = scrapy.Field()
    # 防水功能
    waterproof = scrapy.Field()
    # 摇头功能
    shake = scrapy.Field()
    # 浴居两用
    bath_house = scrapy.Field()
    # 商品链接
    product_url = scrapy.Field()
    # 来源
    source = scrapy.Field()
    # 爬取时间
    ProgramStarttime = scrapy.Field()
