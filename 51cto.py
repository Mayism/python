from urllib import request
import re
import xlrd
import xlwt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Spider():
    """
    爬取51cto网站信息
    """
    # url = f'https://blog.csdn.net/weixin_44708240/article/details/116270210'
    title_root_pattern = '<div class="title">([\s\S]*?)</div>'
    title_pattern = '<h1>([\s\S]*?)</h1>'
    # num_root_pattern = '<div class="bar-content">([\s\S]*?)</div>'
    readNum_pattern = '<b class="fl">([\s\S]*?)</b>'
    crash = 0
    crashnum = 0
    remote = 0
    remotenum = 0
    cloudstorage = 0
    cloudstoragenum = 0
    applinking = 0
    applinkingnum = 0
    apm = 0
    apmnum = 0
    clouddb = 0
    clouddbnum = 0
    quickapp = 0
    quickappnum = 0
    appkit = 0
    appkitnum = 0
    quickgame = 0
    quickgamenum = 0
    auth = 0
    authnum = 0
    cloudfunc = 0
    cloudfuncnum = 0
    opentest = 0
    opentestnum = 0
    sig = 0
    signum = 0
    guideData = 0
    guide = 0
    ques = 0
    quesData = 0

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
        try:
            num = re.findall(Spider.readNum_pattern, htmls)
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
        sheet = worksheet.sheet_by_index(4)
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

    def databyKit(self, title, num):
        try:
            if title.find("崩溃") != -1:
                spider.crash += num
                spider.crashnum += 1
                print("崩溃相关篇数为" + str(spider.crashnum) + "总阅读数为" + str(spider.crash))
            elif title.find("远程配置") != -1:
                spider.remote += num
                spider.remotenum += 1
                print("远程配置相关篇数为" + str(spider.remotenum) + "总阅读数为" + str(spider.remote))
            elif title.find("性能管理") != -1:
                spider.apm += num
                spider.apmnum += 1
                print("性能管理相关篇数为" + str(spider.apmnum) + "总阅读数为" + str(spider.apm))
            elif title.find("AppLinking") != -1:
                spider.applinking += num
                spider.applinkingnum += 1
                print("AppLinking相关篇数为" + str(spider.applinkingnum) + "总阅读数为" + str(spider.applinking))
            elif title.find("云存储") != -1:
                spider.cloudstorage += num
                spider.cloudstoragenum += 1
                print("云存储相关篇数为" + str(spider.cloudstoragenum) + "总阅读数为" + str(spider.cloudstorage))
            elif title.find("云数据库") != -1:
                spider.clouddb += num
                spider.clouddbnum += num
                print("云数据库相关篇数为" + str(spider.clouddbnum) + "总阅读数为" + str(spider.clouddb))
            elif title.find("认证") != -1:
                spider.auth += num
                spider.authnum += 1
                print("认证相关篇数为" + str(spider.authnum) + "总阅读数为" + str(spider.auth))
            elif title.find("快应用") != -1:
                spider.quickapp += num
                spider.quickappnum += 1
                print("快应用相关篇数为" + str(spider.quickappnum) + "总阅读数为" + str(spider.quickapp))
            elif title.find("快游戏") != -1:
                spider.quickgame += num
                spider.quickgamenum += 1
                print("快游戏相关篇数为" + str(spider.quickgamenum) + "总阅读数为" + str(spider.quickgame))
            elif title.find("联运") != -1:
                spider.appkit += num
                spider.appkitnum += 1
                print("联运相关篇数为" + str(spider.appkitnum) + "总阅读数为" + str(spider.appkitnum))
            elif title.find("云函数") != -1:
                spider.cloudfunc += num
                spider.cloudfuncnum += 1
                print("云函数相关篇数为" + str(spider.cloudfunc) + "总阅读数为" + str(spider.cloudfuncnum))
            elif title.find("开放式") != -1:
                spider.opentest += num
                spider.opentestnum += 1
                print("开放式测试相关篇数为" + str(spider.opentest) + "总阅读数为" + str(spider.opentestnum))
            elif title.find("应用签名") != -1:
                spider.sig += num
                spider.signum += 1
                print("应用签名相关篇数为" + str(spider.sig) + "总阅读数为" + str(spider.signum))
        except ValueError as e:
            print(e.__doc__)
            pass

    def painting(self):
        plt.rc('font', family='Youyuan', size='11')  # 和matplotlib一样指明字体
        plt.rc('axes', unicode_minus='False')

        kit = ('崩溃', '性能管理', 'AppLinking', '云存储', '认证', '快应用', '快游戏', '联运', "云函数", "开放式测试", "应用签名")
        num = (spider.crash/spider.crashnum, spider.apm/spider.apmnum, spider.applinking/spider.applinkingnum, spider.cloudstorage/spider.cloudstoragenum, spider.auth/spider.authnum, spider.quickapp/spider.quickappnum, spider.quickgame/spider.quickgamenum, spider.appkit/spider.appkitnum, spider.cloudfunc/spider.cloudfuncnum, spider.opentest/spider.opentestnum, spider.sig/spider.signum)
        pdseries = pd.Series(num, index=kit)
        print(pdseries)
        plt.title('各个kit平均浏览量')  # 设置中文标题
        pdseries.plot(kind='bar', align='center', alpha=0.6, rot=50)
        # pdseries.plot.bar(align='center',alpha=0.6,rot=50)
        plt.show()

    def paintingbykind(self):
        plt.rc('font', family='Youyuan', size='11')  # 和matplotlib一样指明字体
        plt.rc('axes', unicode_minus='False')

        kit = ('解决方案类', '开发指导类')
        num = (spider.quesData, spider.guideData)
        pdseries = pd.Series(num, index=kit)
        print(pdseries)
        plt.title('解决方案及开发指导类总浏览')  # 设置中文标题
        pdseries.plot(kind='bar', align='center', alpha=0.6, rot=50)
        # pdseries.plot.bar(align='center',alpha=0.6,rot=50)
        plt.show()

    def paintingaveragedbykind(self):
        plt.rc('font', family='Youyuan', size='11')  # 和matplotlib一样指明字体
        plt.rc('axes', unicode_minus='False')

        kit = ('解决方案类', '开发指导类')
        num = (spider.quesData / spider.ques, spider.guideData / spider.guide)
        pdseries = pd.Series(num, index=kit)
        print(pdseries)
        plt.title('解决方案及开发指导类总浏览')  # 设置中文标题
        pdseries.plot(kind='bar', align='center', alpha=0.6, rot=50)
        # pdseries.plot.bar(align='center',alpha=0.6,rot=50)
        plt.show()

    def go(self):
        """
        调用正则匹配方法获取想要抓取的数据
        """
        csdn = xlwt.Workbook(encoding='utf-8') #创建Excel
        sheet = csdn.add_sheet('csdn', cell_overwrite_ok = True) #创建sheet页面
        typesheet = self.getType()
        url = self.__getUrl()
        row = 0
        for i in url:
            try:
                cols = typesheet.cell_value(row, 4)
                htmls = self.__fetch_content(i)
                title = self.__getTitle(htmls)
                num = self.__getReadNum(htmls)
                self.databyKit(str(title).split("'")[3], int(str(num).split("'")[3]))
                if int(cols) == 0:
                    spider.guideData += int(str(num).split("'")[3])
                    spider.guide += 1
                else:
                    spider.quesData += int(str(num).split("'")[3])
                    spider.ques += 1
                print('博客:' + str(title).split("'")[3] + ' 阅读量：' + str(num).split("'")[3])
                sheet.write(row, 0, str(title).split("'")[3])
                sheet.write(row, 1, int(str(num).split("'")[3]))
                sheet.write(row, 2, int(cols))
                csdn.save('D:\\pythonProject\\51ctoData.xls')
                row += 1
            except ValueError as e:
                print(e.__doc__+'the error url is' + str(i))
                pass
            print('技术指导类文章数目' + str(spider.guide) + '技术指导类文章浏览:' + str(spider.guideData))
            print('解决方案类文章数目' + str(spider.ques) + '解决方案类文章浏览:' + str(spider.quesData))

# 执行
spider = Spider()
spider.go()
spider.painting()
spider.paintingbykind()
spider.paintingaveragedbykind()
