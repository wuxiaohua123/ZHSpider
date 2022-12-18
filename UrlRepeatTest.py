import pandas as pd
import numpy as np
from itertools import chain

def isRepeat():
    hotLink = pd.read_csv('./事件顺序.csv', usecols=[2])
    hotLink_list = np.array(hotLink).tolist()
    hotLink_one_list = list(chain.from_iterable(hotLink_list))
    print('原文件中URL长度：', len(hotLink_one_list))
    duplicateRemovalList = list(set(hotLink_one_list))
    print('去重后的URL长度：', len(duplicateRemovalList))


def findDuplicateElement():
    hotLink = pd.read_csv('./事件顺序.csv', usecols=[2])
    hotLink_list = np.array(hotLink).tolist()
    hotLink_one_list = list(chain.from_iterable(hotLink_list))
    repeat_url = []
    for url in hotLink_one_list:
        if hotLink_one_list.count(url) > 1:
            repeat_url.append(url)
    print(set(repeat_url))


if __name__ == "__main__" :
    isRepeat()
    findDuplicateElement()