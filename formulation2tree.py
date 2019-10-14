# -*- coding: utf-8 -*-
# 把一个公式转化为二叉树，然后抽取出sum树，替换自定义函数

import re

import self_defined_func as sdf

operatorsPriority = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2, '(': 99, ')': 99, 'sum(': 99, 'avg(': 99, 'std(': 99}
valueType = {'digit': 0, 'variable': 1, 'operation': 2, 'inner_func': 3, 'self_defined_func': 4}


def mid2post(expression):
	result = []
	factorType = []
	operatorStack = []
	index = 0
	expressionLength = len(expression)

	pattern1 = re.compile(r'\d+')
	pattern2 = re.compile(r'[a-z0-9]+')
	
	while index < expressionLength:
		searchStr = expression[index:]
		# 如果是数字则匹配出一串连续数字入结果栈
		if searchStr[0].isdigit():
			factor = re.search(pattern1, searchStr)[0]
			factorLength = len(factor)
			result.append(factor)			
		# 如果是字母则分变量和函数两种情况
		elif searchStr[0].isalpha():
			factor = re.search(pattern2, searchStr)[0]
			factorLength = len(factor)
			# 如果是函数
			if searchStr[factorLength] == '(':			
				factor += '('
				factorLength += 1
				operatorStack.append(factor)			
			else:
				result.append(factor)
		# 如果是+-*/^
		elif searchStr[0] in '+-*/^':
			factor = searchStr[0]
			factorLength = 1
			# 符号栈中优先级不大于操作符的全部出栈，但不包含优先级为3的操作符
			while len(operatorStack) > 0 and operatorsPriority[operatorStack[-1]] >= operatorsPriority[factor] and operatorsPriority[operatorStack[-1]] != 99:
				op = operatorStack.pop()
				result.append(op)
			operatorStack.append(factor)
		# 如果是左括号
		elif searchStr[0] == '(':
			factor = '('
			factorLength = 1
			operatorStack.append(factor)
		# 如果是右括号
		elif searchStr[0] == ')':
			op = operatorStack.pop()
			while operatorsPriority[op] < 99:
				result.append(op)
				op = operatorStack.pop()
			if op != '(':
				result.append(op)
		else:
			print('Unrecognized Pattern!')
			return

		# print('factor = %s' % factor)
		# print('operatorStack = %s' % ','.join(operatorStack))
		# print('result = %s' % ','.join(result))
		
		index += factorLength

	while operatorStack:
		result.append(operatorStack.pop())

	return result


# 树的结点定义
class Node(object):
	def __init__(self, value=None, valueType=None, left=None, right=None):
		self.value = value
		self.valueType = valueType
		self.left = left
		self.right = right


# 因子的数据格式	
def factor2type(factor):
	if factor.isdigit():
		return 0
	elif '(' in factor:
		if factor in sdf.selfDefinedFunc:
			return 4
		else:
			return 3
	elif factor in '+-*/^':
		return 2
	else:
		return 1


# 后缀表达式转换为表达式树
def post2tree(post):
	nodeStack = []
	for item in post:
		itemType = factor2type(item)
		# 操作数为叶子结点
		if itemType == 0 or itemType == 1:
			node = Node(item, itemType, None, None)
		# 操作符含有左右子树		
		elif itemType == 2:
			temp1 = nodeStack.pop()
			temp2 = nodeStack.pop()
			node = Node(item, itemType, temp2, temp1)
		# 函数只有右子树
		else:
			temp = nodeStack.pop()
			node = Node(item, itemType, None, temp)
		nodeStack.append(node)
	return nodeStack[0]


# 中序遍历
def inorder(root):
	if root is None:
		return
	inorder(root.left)
	print('value = %s ' % root.value)
	inorder(root.right)


# 层次遍历，抓出sum函数体
def levelorder2sum(root):
	queue = []
	queue.append(root)
	while queue:
		if queue[0].value == 'sum(':
			return queue[0]
		# print('value = %s \n valueType = %d ' % (queue[0].value, queue[0].valueType))
		if queue[0].left:
			queue.append(queue[0].left)
		if queue[0].right:
			queue.append(queue[0].right)
		queue.pop(0)


if __name__ == '__main__':
	str0 = '1/n*sum(((x-avg(x))/std(x))^4)-3'
	result = mid2post(str0)
	print('result = %s' % ','.join(result))
	tree = post2tree(result)
	
	# preorder(tree)
	sumTree = levelorder2sum(tree)
	
	inorder(sumTree)
