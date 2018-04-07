#coding:utf-8
#!/usr/bin/python

#  图3
#  获得table数据， json格式,
#  对每个excel的数据，获取每年，每个国家的人均gdp和人均消耗量

import os
import  sys
import xlrd
import xlwt
import numpy as np
import json
import Tool.ExcelTool as ExcelTool
import order.settings as Setting

#获得table数据 ，json格式,
def getTableData():

    #print(os.path.join(Setting.FILR_DIR["COMMON_DIR"]))
    files = ExcelTool.listExcelFile(Setting.FILR_DIR["MAP3_DIR"])
    print files             # .xlsx结果文件列表
    resultList = []
    errMsg = ""             #错误信息
    countryNum=189          #国家总数

    for file in files:      # 遍历每个excel文件
        try:
            result = {}     # 单个excel文件处理后的结果
            fullFileName = file.split("\\")[len(file.split("\\")) - 1]
            result["fullFileName"] = fullFileName               # 文件全名 （带后缀）
            result["fileName"] = fullFileName.split(".")[0]     # 文件全名 （不带后缀）
            print file + " start"

            excelData = xlrd.open_workbook(file, "rb")
            # 获取国家名列表
            unit = ''  # 单位
            unitX = ''  # 单位           `
            unitY = ''  # 单位
            country_name = ExcelTool.getArrayBySheetName(os.path.join(Setting.FILR_DIR["COMMON_DIR"], "Countries.xlsx"),"country")
            countryList=[]   #  国家名list，有序
            for i in range(countryNum):
                countryList.append(country_name[i,0].encode("utf-8"))

            timeline=[]                                       #timeline  ,年数的集合
            sheetNameList=excelData.get_sheet_names()         #获取此文件的全部sheet名
            seriesList=[]                                     # series数据，所有年份，所有国家的数据
            for sheetName in sheetNameList:                  #遍历sheet
                if sheetName != 'Unit':                      #处理某年（某sheet）的数据
                    sheetData = ExcelTool.getArrayFromSheet(excelData, sheetName, 'name')   #获取某年（某sheet）的数据
                    series=[]                                 # 某年，所有国家的数据
                    timeline.append(sheetName)                # 年份加入timeline中
                    sheetDataSort=np.argsort(-sheetData ,axis=0 )                          #排序，按列排序，降序
                    sort={}                                                                #排序 ，
                    for i in range(countryNum):
                        sort[sheetDataSort[i][2]]=i+1
                    for j in range(countryNum):
                        seriesCountry=[]                    #某年某个国家的数据
                        seriesCountry.append(sheetData[j][0])           # 人均gdp
                        seriesCountry.append(sheetData[j][1])           # 人均消耗量
                        seriesCountry.append(sheetData[j][2])           # 气泡大小
                        seriesCountry.append(sort[j])                   # 排序号，气泡大小的排序号
                        seriesCountry.append(countryList[j])            # 国家名
                        series.append(seriesCountry)
                    seriesList.append(series)
                else:                                       #处理3个单位
                    unit = excelData.sheet_by_name("Unit").cell_value(0, 1)     # 标题单位
                    unitX = excelData.sheet_by_name("Unit").cell_value(1, 1)    # X轴单位
                    unitY= excelData.sheet_by_name("Unit").cell_value(2, 1)     # Y轴单位

            # 从excel获取sheet， 转化成numpy.array
            result['unit'] = unit                       # 单位
            result['unitX'] = unitX                       # 单位
            result['unitY'] = unitY                       # 单位
            result["counties"]=countryList
            result["timeline"]=timeline
            result["series"]=seriesList

            resultList.append(result)
        except BaseException:
            print "Error: 文件有问题," + file
            print BaseException
            errMsg += file + "<br/>"

    resultListJson = json.dumps(resultList)
    print "Map3返回值 resultListJson :"
    print   resultListJson
    return resultListJson







