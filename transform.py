# -*- coding: utf-8 -*-
# 把sum树转化为聚合因子

import formulation2tree as ft
import self_defined_func as sdf
import aggregates as agg
from model import Model

import math

aggregates = ('x', 'x^2', 'x^3', 'x^4', 'x^5', 'y', 'y^2', 'y^3', 'y^4', 'y^5',
			  'x*y', 'x^2*y', 'x^3*y', 'x^4*y', 'x^5*y', 'x^y*2', 'x^y*3', 'x^y*4', 'x^y*5')

aggregate = ''

test_rows = 10
test_label = ['x']

# parameters
transformable = True
power = []
C = []  
v = []
op = []
sdf_list = []
outer = []


# 中根遍历获取聚合因子 
def inorder2agg(root):
	if root is None:
		return
	inorder2agg(root.left)
	global aggregate
	aggregate += str(root.value)
	inorder2agg(root.right)


# 判断是否为基本聚合因子
def isaggregate(root):
	global aggregate
	inorder2agg(root)
	print('aggregate = %s' % aggregate)
	if aggregate in aggregates:
		aggregate = ''
		return True
	else:
		aggregate = ''
		return False


# 先根遍历，把自定义函数的结点直接进行计算
def preorder2cal(root, label, data):
	if root is None:
		return
	if root.valueType == 4:
		if root.value != 'sum(':
			sdf.func2value(root, label, data)
			return
			# root.left = None
			# root.right = None
			# print('value = %s \n valueType = %d ' % (root.value, root.valueType))
	preorder2cal(root.left, label, data)
	preorder2cal(root.right, label, data)	


# 内置函数的计算
def inner_func(operator, leftnum, rightnum):
	leftnum = float(leftnum)
	rightnum = float(rightnum)
	if operator == '+':
		return leftnum + rightnum
	elif operator == '-':
		return leftnum - rightnum
	elif operator == '*':
		return leftnum * rightnum
	elif operator == '/':
		return leftnum / rightnum
	elif operator == '^':
		return math.pow(leftnum, rightnum)
	else:
		return 0


# 中序遍历从而计算sum树的值
def inorder2cal(root, testdata_i_col):
	if root is None:
		return
	leftnum = inorder2cal(root.left, testdata_i_col)
	operator = root.value
	if root.valueType == 1:
		j = test_label.index(root.value)
		return testdata_i_col[j]
	if root.valueType == 4:
		return sdf.after_cal_sdf[root.value]
	rightnum = inorder2cal(root.right, testdata_i_col)
	if root.left is None and root.right is None:
		return root.value
	else:
		num = inner_func(operator, leftnum, rightnum)
		return num


# sum树求值
def sum2value(root):
	if isaggregate(root.right):
		print("Yes")
	else:		
		testdata = agg.gettestdata('D:/datacanopy/dataset.csv', test_label, test_rows)
		preorder2cal(root, test_label, testdata)
		sumValue = 0
		# print('testdata = ', testdata)
		for i in range(test_rows):
			temp = root.right		
			# 取第i列
			testdata_i_col = [x[i] for x in testdata]
			# print(testdata_i_col)
			tempValue = inorder2cal(temp, testdata_i_col)
			# print('tempValue = %f' % tempValue)
			sumValue += tempValue
		print('sumValue = %f' % sumValue)
		return testdata[0]


# 层次遍历，抓出非计算符号的数值
def levelorder2outer(root, types):
	queue = []
	queue.append(root)
	while queue:
		if queue[0].valueType in types:
			outer.append(queue[0].value)
		elif queue[0].valueType == 1:
			return []
		# print('value = %s \n valueType = %d ' % (queue[0].value, queue[0].valueType))
		if queue[0].left:
			queue.append(queue[0].left)
		if queue[0].right:
			queue.append(queue[0].right)
		queue.pop(0)
	return outer


# 提取所需参数
def sumTree2params(root, isfirst):
	outer_types = [0, 4]
	if root is None:
		return
	if root.value == '^':
		if root.right.valueType == 0:
			op.append('^')
			power.append(root.right.value)
			if isfirst:
				isfirst = False
				# 在第一个^之后紧接着出现了*/，则要判断后续是否有与变量为异侧的因子可以提取出来作为k候选项
				if root.left.value in '*/':
					leftPart = levelorder2outer(root.left.left, outer_types)
					rightPart = levelorder2outer(root.left.right, outer_types)
					outer = leftPart + rightPart
					print('outer = ', outer)
			sumTree2params(root.left, isfirst)
		# 如果指数不为数字则不可转化
		else:
			transformable = False
	elif root.value in '+-*/':
		op.append(root.value)
		sumTree2params(root.left, isfirst)
		sumTree2params(root.right, isfirst)
	elif root.valueType == 0:
		C.append(root.value)
	elif root.valueType == 1:
		v.append(root.value)
	elif root.valueType == 4:
		sdf_list.append(root.value)
	else:
		return 


def printParams():
	print('Transformable = %r' % transformable)
	print('power = %s' % ','.join(power))
	print('constant = %s' % ','.join(C))
	print('variable = %s' % ','.join(v))
	print('operator = %s' % ','.join(op))
	print('sdf = %s' % ','.join(sdf_list))
	print('outer = ', outer)


def main():
	str0 = '1/n*sum(((x-avg(x))/std(x))^4)-3'
	str1 = '1/n*sum(x^2*y)'
	print('initial = %s' % str0)
	result = ft.mid2post(str0)
	print('result = %s' % ','.join(result))
	tree = ft.post2tree(result)

	sumTree = ft.levelorder2sum(tree)

	testdata = sum2value(sumTree)
	ft.inorder(sumTree)
	print('after_cal_sdf = ', sdf.after_cal_sdf)
	sumTree2params(sumTree.right, isfirst=True)
	# printParams()

	if transformable:
		model = Model(power, C, v, op, sdf_list, outer)
		model._gen_params()
		model._print_params()
		model._gen_aggr(testdata)
	else:
		pass


if __name__ == '__main__':
	main()
