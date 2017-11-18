#-*- coding: utf-8 -*-
import urllib.request
import urllib
import http.cookiejar
import urllib.parse
def getOpener(head):
    # deal with the Cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
def my_openurl(url):
    header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Referer': 'jwzx.cqupt.congm.in',
        # 'Accept-Encoding': 'gzip, deflate',
        'Host': '',
        'DNT': '1'
    }
    opener = getOpener(header)
    op = opener.open(url)
    return op