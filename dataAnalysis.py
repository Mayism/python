import pandas as pd

class data():
    #文件路径
    ctoPath = f"D:\\pythonProject\\51ctoData.xls"
    ctoAddress = input(ctoPath)
    csdnPath = f"D:\\pythonProject\\csdnData.xls"
    cnblogPath = f"D:\\pythonProject\\cnblogData.xls"
    oschinaPath = f"D:\\pythonProject\\oschinaData.xls"
    result = []

    def colectData(self):
        df = pd.read_excel(data.ctoAddress, usecols=[0], names=None)
        print("----for test")


#执行
data = data()
data.colectData()

