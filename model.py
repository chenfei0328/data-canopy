# -*- coding: utf-8 -*-
# 建立模型 基本式为：k(c + w1x + w2x2 + w3x3+ w4x4)

import self_defined_func as sdf

from functools import reduce


class Model(object):
    def __init__(self, power, c, v, op, sdf_list, outer):
        self.power = power
        self.C = c
        self.v = v
        self.op = op
        self.sdf_list = sdf_list
        self.outer = outer  # 最外层系数(k)的可能值

        self.product_power = 1  # 所有幂次的乘积
        self.sub_exist = False  # 是否含有减号

    def _print_params(self):
        print('power = %s' % ','.join(self.power))
        print('constant = %s' % ','.join(self.C))
        print('variable = %s' % ','.join(self.v))
        print('operator = %s' % ','.join(self.op))
        print('sdf = %s' % ','.join(self.sdf_list))
        print('outer = ', self.outer)
        print('product_power = %f' % self.product_power)
        print('sub_exist = %r' % self.sub_exist)

    def _gen_params(self):
        if self.power is not []:
            self.product_power = float(reduce(lambda x, y: float(x) * float(y), self.power))
        if '-' in self.op:
            self.sub_exist = True
        if self.outer is not []:
            self.outer = [sdf.after_cal_sdf[s] for s in self.outer if s in sdf.after_cal_sdf]

    def _gen_aggr(self, testdata):
        print('testdata = ', testdata)
        aggr = []
        for n in range(int(self.product_power)):
            temp = [pow(x, n + 1) for x in testdata]
            temp = reduce(lambda x, y: float(x) + float(y), temp)
            aggr.append(temp)
        print('aggr = ', aggr)
