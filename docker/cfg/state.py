from kxi import sp
import pykx 
import numpy as np
import pandas as pd 
import datetime

tp_hostport = ':tp:5010'
kfk_broker  = '104.198.219.51:9091'

lastBidDict = {
    'AAPL': 22.2,
    'IBM': 1112.3
    }

def keep_state(data):
    global lastBidDict
    dict = data.pd()
    if not pd.isna(dict['bid']):
        lastBidDict[dict['sym'].decode()] = dict['bid']
        # print(lastBidDict)
    return lastBidDict

quote_pipeline = (sp.read.from_kafka(topic='quote', brokers=kfk_broker)
    | sp.decode.json()
    | sp.map(keep_state)
    | sp.write.to_console())

sp.run(quote_pipeline)

