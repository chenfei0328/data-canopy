# -*- coding: utf-8 -*-
# 读数据存储因子

import pandas as pd
import random


# 抽取部分原始数据
def gettestdata(path, usecols=None, rows=None):
	data = pd.read_csv(path, usecols=usecols)
	testdata = []
	for item in usecols:
		num = []
		for index in range(rows):		
			num.append(data[item][random.randint(1, len(data) - 1)])
		testdata.append(num)
	return testdata
	


# testdata = gettestdata('D:/datacanopy/dataset.csv', ['x'], 10)
# print(testdata)