from kxi import sp
import pykx as kx
import numpy as np
import pandas as pd 
import datetime

tp_hostport = ':tp:5010'
kfk_broker  = '104.198.219.51:9091'

quote_schema_types = {
    'timestamp':  kx.TimestampAtom,
    'sym':        kx.CharAtom,
    'bid':        kx.FloatAtom,
    'ask':        kx.FloatAtom,
    'bsize':      kx.IntAtom,
    'asize':      kx.IntAtom
}

def transform_quote(data):
    dict = data.pd()
    dict['sym'] = dict['sym'].decode()     ## convert to object - > symbol type
    dict['time'] = dict.pop('timestamp')   ## rename timestamp column
    return dict

quote_pipeline = (sp.read.from_kafka(topic='quote', brokers=kfk_broker)
    | sp.decode.json()
    | sp.transform.schema(table = quote_schema_types)
    | sp.map(transform_quote)
    | sp.map(lambda x: ('quote', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

sp.run(quote_pipeline)