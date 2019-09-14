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
    html = etree.parse(drug_path, etree.HTMLParser())
    info = html.xpath('//div[@class="info-content"]/div[@class="info-left"]')[0]  # /html/body/div[4]/div[1]/div[3]/div[1]/a
    info_text = info.xpath('//div/div[@class="more-infomation"]/p/text()')
    # info_title = info.xpath('//div/div[@class="title"]/a/text()')
    return info_text
# 创建文件
# def create_xlsxfile():
#     drug_word = xlsxwriter.Workbook('语料.xlsx')  # 新建excel表
#     worksheet = drug_word.add_worksheet('sheet1')
# # 写入excel表格
# def write_info(data):
#     drug_word = xlsxwriter.Workbook('语料.xlsx')  # 新建excel表
#     worksheet = drug_word.add_worksheet('sheet1')
#
#     worksheet.write_row("A1", data ,bold)# A1:从A1单元格开始插入数据，按行插入， data:要写入的数据（格式为一个列表), bold:单元格的样式

if __name__ == '__main__':
    drug_word = xlsxwriter.Workbook('语料3.xlsx')  # 新建excel表
    worksheet = drug_word.add_worksheet('sheet1')
    bold = drug_word.add_format({
        'bold': True,  # 字体加粗
        'border': 1,  # 单元格边框宽度
        'align': 'left',  # 水平对齐方式
        'valign': 'vcenter',  # 垂直对齐方式
        # 'fg_color': '#F4B084',  # 单元格背景颜色
        'text_wrap': True,  # 是否自动换行
     })
    path = get_path(r'D:\python\医脉通\医脉通_full.1\西药\泌尿系统药物（完）') # 手动改
    n = 1
    for i in path:
        drug_info = info_extract(i)
        x = 'A'+ str(n)
        worksheet.write_row(x, drug_info, bold)  # A1:从A1单元格开始插入数据，按行插入， data:要写入的数据（格式为一个列表), bold:单元格的样式
        n = n + 1
    drug_word.close()