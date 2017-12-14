import requests
from lxml.etree import HTML as html
url='https://product.suning.com/0070068957/694729819.html'
response=requests.get(url).text
hhh=html(response)
shop_name=hhh.xpath(".//div[@class='si-intro-list']/dl[1]/dd/a/text()")[0]
print(shop_name)