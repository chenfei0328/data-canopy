# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import preprocessing

from functools import reduce
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression


import transform
import formulation2tree as ft
import aggregates as agg

trainSetLen = 1000
testSetLen = 100


def cal_value(root):
    testdata = agg.gettestdata('./dataset.csv', ['x'], 10)
    transform.preorder2cal(root, ['x'], testdata)
    sumValue = 0
    for i in range(10):
        temp = root.right
        testdata_i_col = [x[i] for x in testdata]
        tempValue = transform.inorder2cal(temp, testdata_i_col)
        sumValue += tempValue
    # print('sumValue = %f' % sumValue)
    return sumValue, testdata[0]


def save_data():
    str = '1/n*sum(((x-avg(x))/std(x))^4)-3'
    result = ft.mid2post(str)
    tree = ft.post2tree(result)
    sumTree = ft.levelorder2sum(tree)

    X = []
    y = []
    num = 1000
    for _ in range(num):
        sumValue, testdata = cal_value(sumTree)
        # ft.inorder(sumTree)
        y.append(float(sumValue))
        aggr = []
        for n in range(4):
            temp = [pow(x, n + 1) for x in testdata]
            temp = reduce(lambda a, b: float(a) + float(b), temp)
            aggr.append(temp)
        # print('aggr = ', aggr)
        X.append(aggr)
    xx = np.array(X)
    yy = np.array(y)
    p = int(0.9 * num)
    #print(X)
    #print(y)
    return xx[:p], yy[:p], xx[p:], yy[p:]


def try_different_model(model, x_train, y_train, x_test, y_test):
    model.fit(x_train, y_train)
    score = model.score(x_test, y_test)
    result = model.predict(x_test)
    # print(x_test)
    print(result)

    plt.figure()
    plt.plot(np.arange(len(result)), y_test, 'go-', label='true value')
    plt.plot(np.arange(len(result)), result, 'ro-', label='predict value')
    plt.title('score: %f' % score)
    plt.legend()
    plt.show()


def main():
    x_train, y_train, x_test, y_test = save_data()
    #print(x_train)
    #print(y_train)
    #print(x_test)
    #print(y_test)
    #scaler = preprocessing.StandardScaler().fit(x_train)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_train = min_max_scaler.fit_transform(x_train)
    x_test = min_max_scaler.fit_transform(x_test)
    normalizer = preprocessing.Normalizer().fit(x_train)

    #scaler.transform(x_train)
    normalizer.transform(x_train)
    #scaler.transform(y_train)
    #scaler.transform(x_test)
    normalizer.transform(x_test)
    #scaler.transform(y_test)
    model_SVR = svm.SVR(C=0.4, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
    kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

    try_different_model(model_SVR, x_train, y_train, x_test, y_test)


if __name__ == '__main__':
    main()
