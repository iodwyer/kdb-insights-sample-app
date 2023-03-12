from kxi import sp
import pykx 
import numpy as np
import pandas as pd 

tp_hostport = ':tp:5010'
kfk_broker  = '104.198.219.51:9091'


def transform(data):
    dict = data.pd()
    dict['bsize'] = int(dict['bsize'])
    dict['asize'] = int(dict['asize'])
    dict['time']  = pd.to_datetime(dict['timestamp'].decode("utf-8"))
    dict['sym']   = dict['sym'].decode("utf-8")
    del dict['timestamp'] 
    return dict


# trade_pipeline = (sp.read.from_kafka(topic='trade', brokers=kfk_broker)
#     | sp.decode.json()
#     | sp.map('{[data] (enlist[`timestamp]!enlist `time) xcol enlist "PS*j"$data }')
#     | sp.map(lambda x: ('trade', x))
#     | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

trade_pipeline = (sp.read.from_kafka(topic='trade', brokers=kfk_broker)
    | sp.decode.json()
    | sp.map('{[data] (enlist[`timestamp]!enlist `time) xcol enlist "PS*j"$data }')
    # | sp.map(lambda x: ('trade', x))
    # | sp.write.to_console()
    | sp.write.to_stream(table='trade', stream="dfx-assembly", prefix="rt-"))


# quote_pipeline = (sp.read.from_kafka(topic='quote', brokers=kfk_broker)
#     | sp.decode.json()
#     | sp.map(transform)
#     | sp.map(lambda x: ('quote', x))
#     | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

# sp.run(trade_pipeline, quote_pipeline)
sp.run(trade_pipeline)
# trade_schema = {
#     'timestamp':  'timestamp',
#     'sym':        'symbol',
#     'price':      'float',
#     'size':       'long'
# }

# quote_schema = {
#     'timestamp':  'timestamp',
#     'sym':        'symbol',
#     'bid':        'float',
#     'ask':        'float',
#     'bsize':      'long',
#     'asize':      'long'
# }
