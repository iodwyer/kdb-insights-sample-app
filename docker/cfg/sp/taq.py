from kxi import sp
import pykx
import numpy as np
import pandas as pd 
import datetime

tp_hostport = ':tp:5010'
kfk_broker  = '104.198.219.51:9091'

quote_schema_types = {
    # 'time':       'timestamp',
    # 'sym':        'symbol',
    'bid':        'float',
    'ask':        'float',
    'bsize':      'int64',
    'asize':      'int64'
}

def transform_quote(data):
    dict = data.pd()
    dict['bsize'] = int(dict['bsize'])
    dict['asize'] = int(dict['asize'])
    dict['time']  = dict.pop('timestamp')
    dict['time']  = pd.to_datetime(dict['time'].decode("utf-8"))
    dict['sym']   = dict['sym'].decode("utf-8")
    return dict

# def transform_trade(data):
#     dict = data.pd()
#     # dict['price'] = int(dict['bsize'])
#     dict['size']  = int(dict['size'])
#     dict['time']  = dict.pop('timestamp')
#     dict['time']  = pd.to_datetime(dict['time'].decode("utf-8"))
#     dict['sym']   = dict['sym'].decode("utf-8")
#     # print(dict)
#     return dict

# def transform_quote(data):
#     df = data.pd()
#     print(df)
#     print(type(df))
#     df['time']  = df.pop('timestamp')
#     # df.rename(columns={'timestamp':'time'}, inplace=True)
#     # df.astype(quote_schema_types)
#     df['time']  = pd.to_datetime(df['time'].decode("utf-8"))
#     df['sym']   = df['sym'].decode("utf-8")
#     return df

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
    # print(ohlcv)
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
            'size' : 'sum'
        }
        vwap = df.groupby(['sym', 'time']).apply(lambda x: pd.Series({
            'vwap': (x['price'] * x['size']).sum() / x['size'].sum(),
            'accVol': x['size'].sum()
        }))
        vwap = vwap.reset_index()[['sym', 'time', 'vwap', 'accVol']]
        vwap = vwap.astype({'vwap':'float', 'accVol':'int64'})
        # print(vwap)
    return vwap

trade_source = (sp.read.from_kafka(topic='trade', brokers=kfk_broker)
    | sp.decode.json()
    # | sp.map(transform_trade))
    | sp.map('{[data] enlist "PS*j"$data }') 
    | sp.transform.rename_columns({'timestamp': 'time'}))  ## rename incoming column 'timestamp' to 'time' 

trade_pipeline = (trade_source
    | sp.map(lambda x: ('trade', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

ohlcv_pipeline = (trade_source
    | sp.window.tumbling(period = datetime.timedelta(seconds = 60), time_column = 'time', sort=True)
    | sp.map(ohlcv_agg, name = 'ohlcv')
    | sp.map(lambda x: ('ohlcv', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

vwap_pipeline = (trade_source
    | sp.window.tumbling(period = datetime.timedelta(seconds = 60), time_column = 'time', sort=True)
    | sp.map(vwap_agg)
    | sp.map(lambda x: ('vwap', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

quote_pipeline = (sp.read.from_kafka(topic='quote', brokers=kfk_broker)
    | sp.decode.json()
    | sp.map(transform_quote, name = 'transform quote')
    | sp.map(lambda x: ('quote', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))


sp.run(trade_pipeline, ohlcv_pipeline, vwap_pipeline, quote_pipeline)
# sp.run(test_byte_stream)
# sp.run(quote_pipeline)

#### WIP #####

# #### Issue of second 60 seconds data comes in as type 0h
# ohlcv_sql_pipeline = (trade_source
#     | sp.window.tumbling(period = datetime.timedelta(seconds = 60), time_column = 'time', sort=True)
#     # | sp.map('{[data] show data; data }')
#     | sp.sql("SELECT sym, date_trunc('minute', time), FIRST(price) AS o, MAX(price) AS h, MIN(price) AS l, LAST(price) AS c, SUM(size) AS v from $1 GROUP BY sym, date_trunc('minute', time)")
#     | sp.map(ohlcv_format)
#     # | sp.map('{[data]show meta data; data }')
#     | sp.map(lambda x: ('ohlcv', x))
#     | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))
#     # | sp.write.to_console())

# def ohlcv_format(data):
#     print("$$$$$$$$$$$$$$$$$   type of incoming data: " + str(pykx.q.type(data)) + "  $$$$$$$$$$$$$$$$")
#     df = data.pd()
#     print(df[:2])
#     if df.empty:
#         print('Empty Dataframe')  ## do nothing
#     else:
#         df.rename(columns={'o':'open', 'h':'high', 'l':'low', 'c':'close', 'v':'volume'}, inplace=True, errors='raise')
#     return df

# trade_schema_types = {
#     'timestamp':  'timestamp',
#     'sym':        'symbol',
#     'price':      'float',
#     'size':       'long'
# }

# trade_schema_columns = {
#     'timestamp':  'time',
#     'sym':        'sym',
#     'price':      'price',
#     'size':       'size'
# }
