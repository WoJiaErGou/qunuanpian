import requests
import re
from lxml.etree import HTML
url='https://product.suning.com/0000000000/694729819.html'
response_text=requests.get(url).text
html=HTML(response_text)
try:
    p_Name = re.findall('"itemDisplayName":"(.*?)"', response_text)[0]
except:
    p_Name = None
xxx=html.xpath(".//div[@class='imgzoom-main']/a[@id='bigImg']/img/@alt")[0]
print(xxx)
print(p_Name)
print(len(p_Name))