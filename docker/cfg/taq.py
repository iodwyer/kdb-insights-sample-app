from kxi import sp
import pykx as kx
import numpy as np
import pandas as pd 
import datetime

tp_hostport = ':tp:5010'
kfk_broker  = '104.198.219.51:9091'

quote_schema_types = {
    'timestamp':       'kx.TimestampVector',
    'sym':        'kx.SymbolVector',
    'bid':        'kx.FloatVector',
    'ask':        'kx.FloatVector',
    'bsize':      'kx.IntVector',
    'asize':      'kx.IntVector'
}

def transform_quote(data):
    dict = data.pd()
    dict['bsize'] = int(dict['bsize'])
    dict['asize'] = int(dict['asize'])
    dict['time']  = dict.pop('timestamp')
    dict['time']  = pd.to_datetime(dict['time'].decode("utf-8"))
    dict['sym']   = dict['sym'].decode("utf-8")
    return dict


quote_pipeline = (sp.read.from_kafka(topic='quote', brokers=kfk_broker)
    | sp.decode.json()
    | sp.map('{[x] show x;x}')
    | sp.transform.schema(quote_schema_types)
    | sp.map(lambda x: ('quote', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))


sp.run(quote_pipeline)