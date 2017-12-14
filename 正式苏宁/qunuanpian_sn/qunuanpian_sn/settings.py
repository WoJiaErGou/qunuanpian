# -*- coding: utf-8 -*-
BOT_NAME = 'qunuanpian_sn'
SPIDER_MODULES = ['qunuanpian_sn.spiders']
NEWSPIDER_MODULE = 'qunuanpian_sn.spiders'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 4
suning_user_agent=[
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
FIELDS_TO_EXPORT = [
        'p_Name',  # 商品名称
        'shop_name',  # 店铺名称
        'ProductID',  # 商品ID
        'price',  # 原价
        'PreferentialPrice',  # 折扣价
        'CommentCount',  # 评论总数
        'GoodRateShow',  # 好评率
        'GoodCount',  # 好评
        'GeneralCount',  # 中评
        'PoorCount',  # 差评
        'keyword',  # 评论关键字
        'type',  # 商品详情
        'brand',  # 品牌
        'X_name',  # 型号
        'X_type',  # 类型
        'color',  # 颜色
        'adapt_area',  # 适用面积
        'placement',  # 放置方式
        'heat',  # 加热方式
        'control',  # 控制方式
        'brand_num',  # 加热片数量
        'gear',  # 档位
        'size',  # 产品尺寸
        'dump_off',  # 倾倒断电
        'time',  # 定时功能
        'constant_temp',  # 恒温功能
        'telecontrol',  # 遥控功能
        'waterproof',  # 防水功能
        'shake',  # 摇头功能
        'bath_house',  # 浴居两用
        'product_url',  # 商品链接
        'source',  # 来源
        'ProgramStarttime'  # 爬取时间
]
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'qunuanpian_sn.middlewares.SuningUseragentMiddleware':400,
    'qunuanpian_sn.middlewares.Exceptions':300,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware':True

}
RETRY_ENABLED=True
RETRY_TIMES=3
DOWNLOAD_TIMEOUT = 10
ITEM_PIPELINES = {
    'qunuanpian_sn.pipelines.CSVPipeline':200,
    'qunuanpian_sn.pipelines.MongoPipeline':190,

}
AUTOTHROTTLE_ENABLED = True
MONGO_HOST = "172.28.171.13"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "QNQ"  # 库名
MONGO_COLL = "qnq_sn"  # 文档(相当于关系型数据库的表名)