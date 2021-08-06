import string
from urllib import request
import re
from urllib.request import Request, urlopen

import urllib3
import xlrd
import xlwt

class Spider():
    """
    爬取oschina网站信息
    """
    # url = f'https://blog.csdn.net/weixin_44708240/article/details/116270210'
    title_root_pattern = '<h1 class="article-box__title">([\s\S]*?)</h1>'
    title_pattern = '<a href="([\s\S]*?)" target="_blank">([\s\S]*?)</a>'
    # num_root_pattern = '<div class="bar-content">([\s\S]*?)</div>'
    readNum_pattern = '<div class="item lm">([\s\S]*?)</div>'

    def __fetch_content(self, url):
        """
        docstring
        """
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
            """
            构造请求
            """
            request = Request(url, headers=headers)
            htmls = urlopen(request).read()
            htmls = str(htmls, encoding='utf-8')
            return htmls
        except ValueError as e:
            print(e.__doc__ + 'the error url of 403 is' + str(url))


    def __getTitle(self, htmls):
        titles = []
        root_html = re.findall(Spider.title_root_pattern, htmls)
        try:
            for html in root_html:
                title = re.findall(Spider.title_pattern, html)
                data = {'title': title}
                titles.append(data)
                print(title)
        except ValueError as e:
            print(e.__doc__ + 'the error title is' + str(title))
            pass
        return titles


    def __getReadNum(self, htmls):
        nums = []
        try:
            num = re.findall(Spider.readNum_pattern, htmls)
            data = {'num': num}
            nums.append(data)
        except ValueError as e:
            print(e.__doc__ + 'the error num is' + str(num))
            pass
        return nums


    def __getUrl(self):
        worksheet = xlrd.open_workbook('D:\sheet.xls')
        sheet_names = worksheet.sheet_names()
        print(sheet_names)
        sheet = worksheet.sheet_by_index(1)
        """
           获取csdn sheet的url列，此处我的列为3
        """
        rows = sheet.nrows
        cols = sheet.ncols
        all_content = []
        for i in range(rows):
            cell = sheet.cell_value(i, 3)
            try:
                cell = str(cell)
                all_content.append(cell)
            except ValueError as e:
                pass
        return all_content

    def getType(self):
        worksheet = xlrd.open_workbook('D:\sheet.xls')
        sheet_names = worksheet.sheet_names()
        print(sheet_names)
        sheet = worksheet.sheet_by_index(4)
        return sheet

    def __sort(self, datas):
        """
        排序
        """
        datas = sorted(datas, key=self.__sort_seed, reverse=True)
        # datas = sorted(datas,key=lambda data: int(data['num'][0]),reverse=True)
        return datas

    def __sort_seed(self, data):
        """
        自定义排序方法
        """
        # r = re.findall(data['num'][0])
        number = int(data['num'])
        return number

    def go(self):
        """
        调用正则匹配方法获取想要抓取的数据
        """
        csdn = xlwt.Workbook(encoding='utf-8') #创建Excel
        sheet = csdn.add_sheet('csdn', cell_overwrite_ok = True) #创建sheet页面
        typesheet = self.getType()
        url = self.__getUrl()
        guideData = 0;
        guide = 0
        ques = 0
        quesData = 0
        row = 0
        for i in url:
            try:
                cols = typesheet.cell_value(row, 4)
                htmls = self.__fetch_content(i)
                title = self.__getTitle(htmls)
                num = self.__getReadNum(htmls)
                num = str(num).split("'")[5].split(" ")[1]
                # if int(cols) == 0:
                #     if num.endswith('K'):
                #         guideData += int(num) * 1000
                #     elif num.endswith('W'):
                #         guideData += int(num) * 10000
                #     else:
                #         guideData += int(num)
                #     guide += 1
                #     print('技术指导类文章数目' + str(guide) + '技术指导类文章浏览:' + str(guideData))
                # else:
                #     if num.endswith('K'):
                #         quesData += int(num) * 1000
                #     elif num.endswith('W'):
                #         quesData += int(num) * 10000
                #     else:
                #         quesData += int(num)
                #     ques += 1
                #     print('解决方案类文章数目' + str(ques) + '解决方案类文章浏览:' + str(quesData))
                print('博客:' + str(title).split("'")[5] + ' 阅读量：' + str(num))
                sheet.write(row, 0, str(title).split("'")[5])
                sheet.write(row, 1, num)
                # sheet.write(row, 2, int(cols))
                """
                保存路径需要自定义
                """
                csdn.save('D:\\pythonProject\\oschinaData.xls')
                row += 1
            except ValueError as e:
                print(e.__doc__+'the error url is' + str(i))
                pass


# 执行
spider = Spider()
spider.go()
