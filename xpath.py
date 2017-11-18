# encoding:utf-8
import lib.curl as curl
from lxml import etree

url = 'http://zycq.cn/index/index/volunteer_info?uid=1865867'

# html = curl.my_openurl(url).read().decode('gbk')
file = open('./content.html', 'rb')
html = file.read().decode('utf8')
file.close()
# print(html)
tree = etree.HTML(html)

# content = tree.xpath('//div[@class="wb50 fl"]')
content = tree.xpath('//tbody')
for each in content:
    # print(each.xpath('string()'))
    list = each.xpath('//td/text()')
    for str in list:
        print(str)

file = "*"
table = "liu"
more = "where id=1"
str = "select %s from %s %s" % (file,table,more)

print(str)