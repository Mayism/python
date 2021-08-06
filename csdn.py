from urllib import request
import re
import xlrd
import xlwt

class Spider():
    """
    爬取csdn网站信息
    """
    # url = f'https://blog.csdn.net/weixin_44708240/article/details/116270210'
    title_root_pattern = '<div class="article-title-box">([\s\S]*?)</div>'
    title_pattern = '<h1 class="title-article" id="articleContentId">([\s\S]*?)</h1>'
    num_root_pattern = '<div class="bar-content">([\s\S]*?)</div>'
    readNum_pattern = '<span class="read-count">([\s\S]*?)</span>'
    page = 1

    def __fetch_content(self, url):
        """
        docstring
        """
        try:
            r = request.urlopen(url)
            htmls = r.read()
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
        except ValueError as e:
            print(e.__doc__ + 'the error title is' + str(title))
        return titles


    def __getReadNum(self, htmls):
        nums = []
        root_html = re.findall(Spider.num_root_pattern, htmls)
        try:
            for html in root_html:
                num = re.findall(Spider.readNum_pattern, html)
                data = {'num': num}
                nums.append(data)
        except ValueError as e:
            print(e.__doc__ + 'the error num is' + str(num))

        return nums

    def __refine(self, datas):
        """
        将抓取的数据进行美化
        """
        l = lambda data: {
            'title': data['title'][0].strip() if len(data['title']) != 0 else '无标题',
            'num': data['num'][0]
        }
        return map(l, datas)

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

    def __show(self, datas):
        """
        数据展示
        """
        for rank in range(0, len(datas)):
            print('排名:' + str(rank + 1)
                  + '   博客：' + datas[rank]['title']
                  + '   阅读量：' + datas[rank]['num'])

    def __getUrl(self):
        worksheet = xlrd.open_workbook('D:\sheet.xls')
        sheet_names = worksheet.sheet_names()
        print(sheet_names)
        sheet = worksheet.sheet_by_index(2)
        """
           获取csdn sheet的url列
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
                # cols = typesheet.cell_value(row, 4)
                htmls = self.__fetch_content(i)
                title = self.__getTitle(htmls)
                num = self.__getReadNum(htmls)
                # if int(cols) == 0:
                #     guideData += int(str(num).split("'")[3])
                #     guide += 1
                #     print('技术指导类文章数目' + str(guide) + '技术指导类文章浏览:' + str(guideData))
                # else:
                #     quesData += int(str(num).split("'")[3])
                #     ques += 1
                #     print('解决方案类文章数目' + str(ques) + '解决方案类文章浏览:' + str(quesData))
                print('博客:' + str(title).split("'")[3] + ' 阅读量：' + str(num).split("'")[3])
                sheet.write(row, 0, str(title).split("'")[3])
                sheet.write(row, 1, int(str(num).split("'")[3]))
                # sheet.write(row, 2, int(cols))
                csdn.save('D:\\pythonProject\\csdnData.xls')
                row += 1
            except ValueError as e:
                print(e.__doc__+'the error url is' + str(i))
                pass


# 执行
spider = Spider()
spider.go()
