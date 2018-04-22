#coding:utf-8
#!/usr/bin/python

# excel文件操作工具类
# 依赖    xlrd、xlwt、 numpy
import os
import os.path
import  sys
import xlrd
import xlwt
import numpy as np



#   从根目录下读取指定的excel数据
def getArrayBySheetName(excelDir,sheetName):
    excelData = xlrd.open_workbook(excelDir, "rb")
    Country_array = getArrayFromSheet(excelData,sheetName,'name')
    return Country_array

# 读取根目录下制定的excel数据
def getArrayBySheetIndex(excelDir,index):
    excelData = xlrd.open_workbook(excelDir, "rb")
    Country_array = getArrayFromSheet(excelData,index,'index')
    return Country_array


#   根据sheetName或者sheetIndex从excel获取sheet， 转化成 numpy.array
#   excelData: excel数据
#   type:      "name" 或"index"
#   param   :sheet的索引或名称
#   row     :可以指定长度，相当于切片。默认是sheet的行
#   column  :可以指定长度，相当于切片。默认是sheet的列
def getArrayFromSheet(excelData,param ,type,row=0,column=0):
    if(type=='index'):
        sheet = excelData.sheet_by_index(param)
    elif(type=='name'):
        sheet=excelData.sheet_by_name(param)
    if not (row!=0 and row<sheet.nrows):
        row=sheet.nrows
    if not(column!=0 and column<sheet.ncols):
        column = sheet.ncols  # 列
    _array=[]
    for i in range(0,row):
        _row=[]
        for j in range(0, column):
            _row.append(sheet.cell_value(i,j))
        _array.append(_row)
    np_array = np.array(_array)
    return np_array



#   获取根目录下，指定目录中 excel文件的地址列表  ，只获取xls和xlsx文件
#   dir: 指定的目录
def listExcelFile( dir ):
    res=[]
    for root, dirs, files in os.walk(dir):
        for file in files:
            try:
                if os.path.splitext(file)[1] == '.xlsx' or  os.path.splitext(file)[1] == '.xls':
                    res.append(os.path.join(root, file))
            except BaseException:
                print "Error:！文件读取失败：" + file
    return res



#   删除指定目录下的指定文件
#   address :      根目录下的指定目录
#   fileNameList : 要删除的文件名  如 “文件1.xls,文件2.xlsx,文件3.xlsx,文件4.xlsx”
def deleteFile(address,fileNameList ):
    nameList=fileNameList.split(",")
    resString=""
    for fileName in nameList:
        file_address=os.path.join(address,fileName)
        os.remove(file_address)
        resString=resString+",<br>"+fileName
    resString=resString[1:len(resString)]
    return "以下数据文件删除成功："+resString





