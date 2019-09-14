from lxml import etree
import os
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

#获取文件路径
def get_path(pamename):
    file_name = []
    for root, dirs, files in os.walk(pamename):
        for name in files:
            file_name.append(os.path.join(root, name))
    return file_name


# 提取信息
def info_extract(drug_path):
    tittle_list = [] # 没有分类标签
    drug_info = []
    drug = dict()
    html = etree.parse(drug_path, etree.HTMLParser())
    info = html.xpath('//div[@class="info-content"]/div[@class="info-left"]')[0]
    info_title = info.xpath('//div/div[@class="title"]/a')# /html/body/div[6]/div[1]/div[2]/div[1]/a
    for i in info_title:
        x = i.xpath('string(.)')
        x = x.strip('\r')
        x = x.strip('\n')
        x = x.strip('\t')
        x = x.strip()
        tittle_list.append(x)
    info_text = info.xpath('//div/div[@class="more-infomation"]')  # /html/body/div[4]/div[1]/div[2]/div[2]/p[1]/text()
    for t in info_text:
        t = t.xpath('string(.)')
        t = t.replace('\t', '')
        t = t.replace('\r', '')
        t = t.replace('\r', '')
        t = t.replace(' ', '')
        drug_info.append(t)
    for z in range(len(tittle_list)):
        drug[tittle_list[z]] = drug_info[z]
    # for i in info_text:
    #     i = i.strip('\r')
    #     i = i.strip('\n')
    #     i = i.strip('\t')
    #     i = i.strip('>>')
    #     i = i.strip()
    #     info_text[z] = i
    #     z += 1
    # info_cate = info.xpath('//div/div[@class="more-infomation"]/p/a[@class="have-h"]/text()')
    # for i in info_cate:
    #     i = i.strip('\r')
    #     i = i.strip('\n')
    #     i = i.strip('\t')
    #     info_cate[x] = i
    #     x += 1
    # info_cate = set(info_cate)
    return drug

if __name__ == '__main__':
    path = get_path(r'D:\python\医脉通\医脉通_full.1\西药\循环系统药物（完）') # 手动改
    fw = open("druginfo循环系统药物（完）.txt", 'w+',encoding='utf-8') # 手动改
    for i in path:
        drug_info = info_extract(i)
        fw.write('\n' + str(drug_info))  # 把字典转化为str
    fw.close()
