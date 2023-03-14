from kxi import sp
import pykx 
import numpy as np
import pandas as pd 
import datetime

tp_hostport = ':tp:5010'
kfk_broker  = '104.198.219.51:9091'


def transform_quote(data):
    dict = data.pd()
    dict['bsize'] = int(dict['bsize'])
    dict['asize'] = int(dict['asize'])
    dict['time']  = pd.to_datetime(dict['timestamp'].decode("utf-8"))
    dict['sym']   = dict['sym'].decode("utf-8")
    del dict['timestamp'] 
    return dict

def ohlcv_agg(data):
    df = data.pd()
    # create datetime column
    df['time'] = df['time'].dt.floor('min')
    # group by sym and datetime, and aggregate
    agg = {
        'price': ['first', 'max', 'min', 'last'],
        'size': 'sum'
    }
    ohlcv = df.groupby(['sym', 'time']).agg(agg)
    # rename columns to match KDB/Q query
    ohlcv.columns = ['open', 'high', 'low', 'close', 'volume']
    # reset index to make columns sym and datetime
    ohlcv = ohlcv.reset_index()[['sym', 'time', 'open', 'high', 'low', 'close', 'volume']]
    ohlcv = ohlcv.astype({'open':'float', 'high':'float','low':'float','close':'float','volume':'int64'})
    print(ohlcv)
    return ohlcv

def vwap_agg(data):
    df = data.pd()

    if df.empty:
        # print('Empty Dataframe')
        vwap = df
    else:
        # create datetime column
        df['time'] = df['time'].dt.floor('min')

        # group by sym and datetime, and calculate VWAP and accumulated volume
        agg = {
            'price': 'mean',
            'size': 'sum'
        }
        vwap = df.groupby(['sym', 'time']).apply(lambda x: pd.Series({
            'vwap': (x['price'] * x['size']).sum() / x['size'].sum(),
            'accVol': x['size'].sum()
        }))
        vwap = vwap.reset_index()[['sym', 'time', 'vwap', 'accVol']]
        vwap = vwap.astype({'vwap':'float', 'accVol':'int64'})
        print(vwap)
    return vwap

trade_source = (sp.read.from_kafka(topic='trade', brokers=kfk_broker)
    | sp.decode.json()
    | sp.map('{[data] (enlist[`timestamp]!enlist `time) xcol enlist "PS*j"$data }'))

trade_pipeline = (trade_source
    | sp.map(lambda x: ('trade', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

ohlcv_pipeline = (trade_source
    | sp.window.tumbling(period = datetime.timedelta(seconds = 60), time_column = 'time', sort=True)
    | sp.map(ohlcv_agg)
    | sp.map(lambda x: ('ohlcv', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

vwap_pipeline = (trade_source
    | sp.window.tumbling(period = datetime.timedelta(seconds = 60), time_column = 'time', sort=True)
    | sp.map(vwap_agg)
    | sp.map(lambda x: ('vwap', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

quote_pipeline = (sp.read.from_kafka(topic='quote', brokers=kfk_broker)
    | sp.decode.json()
    | sp.map(transform_quote)
    | sp.map(lambda x: ('quote', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

sp.run(trade_pipeline, ohlcv_pipeline, vwap_pipeline, quote_pipeline)

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
