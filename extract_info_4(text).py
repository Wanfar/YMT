from lxml import etree
import os
import xlsxwriter

#获取文件路径
def get_path(pamename):
    file_name = []
    for root, dirs, files in os.walk(pamename):
        for name in files:
            file_name.append(os.path.join(root, name))
    return file_name

# 提取信息
def info_extract(drug_path):
    drug = []
    html = etree.parse(drug_path, etree.HTMLParser())
    info = html.xpath('//div[@class="info-content"]/div[@class="info-left"]')[0]  # /html/body/div[4]/div[1]/div[3]/div[1]/a
    info_text = info.xpath('//div/div[@class="more-infomation"]/p')
    for t in info_text:
        t = t.xpath('string(.)')
        t = t.replace('\t', '')
        t = t.replace('\r', '')
        t = t.replace('\r', '')
        t = t.replace(' ', '')
        drug.append(t)
    # info_title = info.xpath('//div/div[@class="title"]/a/text()')
    return drug

if __name__ == '__main__':
    path = get_path(r'D:\python\医脉通\医脉通_full.1\西药\代谢及内分泌系统药物（完）') # 手动改
    fw = open("test_3.txt", 'w+', encoding='utf-8')
    for i in path:
        drug_info = info_extract(i)
        for m in drug_info:
            fw.write('\n' + m)  # 把字典转化为str
    fw.close()