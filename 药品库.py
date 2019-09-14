import requests
import re
import os
import time

'''
医脉通：一共x页药品，每页10种药
1、先构造每一主页的url,“start_url+&page=x"  first_url_list[]
2、从每一页主页中提取药品的url drug_url[]
3、请求返回药品的源代码 drug_info.txt
每类药品新建一个文件
'''

start_url = 'http://drugs.medlive.cn/drugref/drugCateLast.do?treeCode=Z0201'
# 可更改！！treeCode="....."是医脉通的药品类别的主页


def get_source(url):
    """
    获取网页源代码。
    :param url: 网址
    :return: 网页源代码
    """
    html = requests.get(url).content.decode()
    time.sleep(2)
    return html


def make_url(html):
    """
    html即start_url
    构造主页url
    """
    first_url_list = []
    first_url_list.append(html)
    mainurl_0 = html + '&page='
    for i in range(2, 23):  # 按实际药品主页页数而定
        mainurl = mainurl_0 + str(i)
        first_url_list.append(mainurl)
    return first_url_list


def get_drugurl(html_txt):
    """
    请求返回主页的源代码
    用xpath获得药品的链接
    """
    url_0 = re.search('该分类下共有药品(.*?)京ICP备13043379号-5', html_txt, re.S).group(1)  # 先抓大再抓小
    url_1 = re.findall('<a target="_blank" href=(.*?)>', url_0, re.S)
    drugurl_list = []
    for i in url_1:
        i = i.replace('\'', '')
        i = 'http://drugs.medlive.cn/' + i
        drugurl_list.append(i)
    drug_name_0 = re.findall('shtml\'>(.*?)</a>', url_0, re.S)
    drug_name_1 = []
    for i in drug_name_0:
        i = i.replace('\n', '')
        i = i.replace('\t', '')
        i = i.replace(' ', '')
        i = i.replace('\r', '')
        # i = i.replace('\\', '')
        i = i.replace('-', '.')  # !!有‘-’的都换成'.'
        i = i.replace('/', '_')  # !!有‘/’的都换成'_'
        i = i.replace('<', '(')  # !!有‘<’的都换成'('
        i = i.replace('>', ')')  # !!有‘>’的都换成')'
        drug_name_1.append(i)
    return drugurl_list, drug_name_1


def save(drugname, drug_info):
    """
    将每一页的网页的源代码保存到本地
    """
    os.makedirs('内科用药(中成药)', exist_ok=True)   # 如果没有"医脉通文件夹，就创建一个，如果有，则什么都不做"（可更改名字）
    x = 0
    for i in drugname:
        with open(os.path.join('内科用药(中成药)', i + '.txt'), 'w', encoding='utf-8') as f:  # 名字可更改
            f.write(drug_info[x])
            x = x+1


def get_druginfo(drug_url_list):
    drug_info_list = []
    for i in drug_url_list:
        drug_info_list.append(requests.get(i).content.decode())
        time.sleep(1)
    return drug_info_list


if __name__ == '__main__':
    page_link = make_url(start_url)
    page_link_list = make_url(start_url)
    # page_link_list = page_link_list[13:]  # 第一次爬的时候不要用，中断之后按爬了多少页进行切片继续
    for i in page_link_list:
        d_url, d_name = get_drugurl(get_source(i))
        d_info = get_druginfo(d_url)
        save(d_name, d_info)
        time.sleep(2)
