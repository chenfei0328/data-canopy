# -*- coding: utf-8 -*-
# 创建数据集

import pandas as pd
import numpy as np


def create():
	np.random.seed(1)
	nor1 = np.random.normal(loc=20, scale=10, size=1000)

	np.random.seed(2)
	nor2 = np.random.normal(loc=10, scale=2, size=1000)

	submission = pd.DataFrame({'x': nor1, 'y': nor2})
	submission.to_csv('./dataset.csv', index=False)


create()
