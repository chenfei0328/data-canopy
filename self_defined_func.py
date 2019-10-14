# -*- coding: utf-8 -*-
# 自定义函数的定义和计算

import numpy as np

selfDefinedFunc = ('sum(', 'avg(', 'std(')
after_cal_sdf = {}


def avg(data):
	return


def std(data):
	return


# 自定义函数直接求值
def func2value(node, label, data):
	value = 0
	i = label.index(node.right.value)
	temp = np.array(data[i])
	if node.value == 'avg(':		
		value = np.mean(temp)
		after_cal_sdf['avg('] = value
	elif node.value == 'std(':
		value = np.std(temp)
		after_cal_sdf['std('] = value
	else:
		pass
