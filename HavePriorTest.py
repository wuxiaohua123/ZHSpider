import pandas as pd
import numpy as np


def HavePriorId():
    dataframe = pd.read_csv('./事件顺序.csv')
    havePriorIdUrl = []
    for index, row in dataframe.iterrows():
        if(not np.isnan(row['hotPriorId'])):
            # print(index, row['hotId'], row['hotPriorId'], row['hotLink'])
            havePriorIdUrl.append(row['hotLink'])
    print(len(havePriorIdUrl))


def OldlyEventId():
    dataframe = pd.read_csv('./事件顺序.csv')
    hotPriorId = np.array(dataframe['hotPriorId']).tolist()
    oldlyEventId = []
    for index, row in dataframe.iterrows():
        if(np.isnan(row['hotPriorId'])):
            if(row['hotId'].isdigit() and float(row['hotId']) in hotPriorId):
                # print(index, row['hotId'], row['hotPriorId'], row['hotLink'])
                oldlyEventId.append(row['hotLink'])
    print(len(oldlyEventId))


def LastlyEventId():
    dataframe = pd.read_csv('./事件顺序.csv')
    hotPriorId = np.array(dataframe['hotPriorId']).tolist()
    LastlyEventId = []
    for index, row in dataframe.iterrows():
        # 最新事件 = 有过去事件 + 无后续事件
        if(not np.isnan(row['hotPriorId'])):
            if(float(row['hotId']) not in hotPriorId):
                # print(index, row['hotId'], row['hotPriorId'], row['hotLink'])
                LastlyEventId.append(row['hotLink'])
    print(len(LastlyEventId))


def IdEqualPriorId():
    dataframe = pd.read_csv('./事件顺序.csv', dtype = str)
    idEqualPriorId = []
    for index, row in dataframe.iterrows():
        if(row['hotId'] == row['hotPriorId']):
            # print(index, row['hotId'], row['hotPriorId'], row['hotLink'])
            idEqualPriorId.append(row['hotLink'])
    print(len(idEqualPriorId))

if __name__ == "__main__" :
    HavePriorId()
    LastlyEventId()
    OldlyEventId()
    IdEqualPriorId()