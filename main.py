# encoding:utf-8
import re
import urllib.request
import urllib
import http.cookiejar
import urllib.parse
import json

from collections import deque
import pymysql


def saveFile(file_path, data):
    save_path = file_path
    print('记录日志:' + file_path)
    f_obj = open(save_path, 'a+')  # wb 表示打开方式
    f_obj.write(data + '\r\n')
    f_obj.close()


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


def insert_db(db, json_str):
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    json_obj = json.loads(json_str)
    sql = "insert into t_volunteer.t_volunteer_info set v_uid=\"" + json_obj['v_id'] + "\", " + "v_name=\"" + json_obj[
        'name'] + "\", v_sex=\"" + json_obj['sex'] + "\", v_volunteer_time=\"" + json_obj[
              'volunteer_time'] + "\", v_organization_oid=\"" + json_obj['organization'][
              'o_id'] + "\", v_organization_name=\"" + json_obj['organization'][
              'o_name'] + "\", v_info_json=\"" + db.escape_string(json_str) + "\""
    saveFile('./log/insert_sql.log', sql)
    # value = db.escape_string(value)
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    db.commit()


def GetMiddleStr(content, startStr, endStr):
    startIndex = content.index(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
    endIndex = content[startIndex:].index(endStr)
    return content[startIndex:][:endIndex]


def get_volunteer_info(data):
    result = GetMiddleStr(data, '编号', '个人动态')
    v_id = GetMiddleStr(result, "</span> ", "</p></div>")
    name = GetMiddleStr(result, '姓名：</span>', '</p>')
    volunteer_time = GetMiddleStr(result, '服务时间：</span>', '</p>')
    sex = GetMiddleStr(result, '性别：</span>', '</p>')
    organization_id = GetMiddleStr(result, "oid=", "\" class=\"")
    organization_name = GetMiddleStr(result, "class=\"black\"> ", "</a><br/>")
    volunteer_info = {'v_id': v_id, 'name': name, 'volunteer_time': volunteer_time, 'sex': sex,
                      'organization': {'o_id': organization_id, 'o_name': organization_name}}
    info_json = json.dumps(volunteer_info, ensure_ascii=False)
    return info_json


def add_to_queue(url):
    if url not in visited:
        queue.append(url)
        print('加入队列 --->  ' + url)


# 打开数据库连接
db = pymysql.connect("127.0.0.1", "root", "", "t_volunteer", charset="utf8")

queue = deque()
visited = set()
# kebiao_url = 'http://jwzx.cqupt.congm.in/jwzxtmp/kebiao/kb_stu.php?xh='
# base_url = 'http://jwzx.cqupt.congm.in/jwzxtmp/'
# url = 'http://jwzx.cqupt.congm.in/jwzxtmp/pubBjsearch.php?action=bjStu'  # 入口页面, 可以换成别的
person_url = 'http://zycq.cn/index/index/volunteer_info?'
url = 'http://zycq.cn/index/index/org_info?oid=2546'
organ_url = 'http://zycq.cn/index/index/org_info?'

queue.append(url)
cnt = 0

while queue:
    url = queue.popleft()  # 队首元素出队
    saveFile('./log/visit_url.log', url)
    visited |= {url}  # 标记为已访问
    print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
    cnt += 1
    # urlop = urllib.request.urlopen(url)
    urlop = my_openurl(url)
    if 'html' not in urlop.getheader('Content-Type'):
        print('html not in ERROR')
        continue
    # 避免程序异常中止, 用try..catch处理异常
    try:
        data = urlop.read().decode('utf-8')
        if ('oid' in url):
            saveFile('./log/organization.log', url)
            # 挂靠组织信息，抓取组织下的成员uid加入队列
            uidlist = re.compile('uid=[0-9]{0,10}')
            for uid in uidlist.findall(data):
                add_to_queue(person_url + uid)
        if ('uid' in url):
            # 成员信息，获取成员信息，并把挂靠组织加入搜索队列
            saveFile('./log/volunteer_info.log', url)
            info_json = get_volunteer_info(data)
            insert_db(db, info_json)
            oidlist = re.compile('oid=[0-9]{0,10}')
            for oid in oidlist.findall(data):
                print('===================================================' + oid)
                add_to_queue(organ_url + oid)
        else:
            pass
            # print(data)
            #     saveFile(str(cnt), data)
    except:
        continue
