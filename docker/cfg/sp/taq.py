from kxi import sp
import pykx as kx
import numpy as np
import pandas as pd 
import datetime

tp_hostport = ':tp:5010'

kfk_broker  = 'kafka.trykdb.kx.com:443'
kfk_broker_options = {
    'sasl.username': 'demo',
    'sasl.password': 'demo',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'security.protocol': 'SASL_SSL'}

quote_schema_types = {
    'time':     kx.TimestampAtom,
    'sym':      kx.SymbolAtom,
    'bid':      kx.FloatAtom,
    'ask':      kx.FloatAtom,
    'bsize':    kx.LongAtom,
    'asize':    kx.LongAtom
}

trade_schema_types = {
    'time':     kx.TimestampAtom,
    'sym':      kx.SymbolAtom,
    'price':    kx.FloatAtom,
    'size':     kx.LongAtom
}

def transform_dict_to_table(d):     ## transform dictionary to table object
    return kx.q.enlist(d)   

def ohlcv_agg(data):
    sql_query = """
        SELECT 
            date_trunc('second', time), 
            sym, 
            FIRST(price) AS OPEN, 
            MAX(price)   AS HIGH, 
            MIN(price)   AS LOW, 
            LAST(price)  AS CLOSE_X, 
            SUM(size)    AS VOL 
        FROM $1 
        GROUP BY sym, date_trunc('second', time)
        """
    return kx.q.sql(sql_query, data)

def vwap_agg(data):
    sql_query = """
        SELECT 
            date_trunc('second', time), 
            sym, 
            SUM(price * size) / SUM(size)   AS vwap,
            SUM(size)                       AS accVol
        FROM $1 
        GROUP BY sym, date_trunc('second', time)
        """
    return kx.q.sql(sql_query, data)

trade_source = (sp.read.from_kafka(topic='trade', brokers=kfk_broker, options=kfk_broker_options)
    | sp.decode.json()
    | sp.map(transform_dict_to_table, name = 'transform trade')
    | sp.transform.rename_columns({'timestamp': 'time'})          ## rename incoming column 'timestamp' to 'time' 
    | sp.transform.schema(trade_schema_types))

trade_pipeline = (trade_source
    | sp.map(lambda x: ('trade', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

ohlcv_pipeline = (trade_source
    | sp.window.tumbling(period = datetime.timedelta(seconds = 60), time_column = 'time', sort=True)
    | sp.map(ohlcv_agg, name = 'ohlcv')
    | sp.transform.rename_columns({'OPEN': 'open', 'HIGH': 'high', 'LOW': 'low', 'CLOSE_X': 'close', 'VOL': 'volume'})  
    | sp.map(lambda x: ('ohlcv', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

vwap_pipeline = (trade_source
    | sp.window.tumbling(period = datetime.timedelta(seconds = 60), time_column = 'time', sort=True)
    | sp.map(vwap_agg)
    | sp.map(lambda x: ('vwap', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))

quote_pipeline = (sp.read.from_kafka(topic='quote', brokers=kfk_broker, options=kfk_broker_options)
    | sp.decode.json()
    | sp.map(transform_dict_to_table, name = 'transform quote')
    | sp.transform.rename_columns({'timestamp': 'time'})
    | sp.transform.schema(quote_schema_types)
    | sp.map(lambda x: ('quote', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.upd', spread=True))


sp.run(trade_pipeline, ohlcv_pipeline, vwap_pipeline, quote_pipeline)


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
#     print("$$$$$$$$$$$$$$$$$   type of incoming data: " + str(kx.q.type(data)) + "  $$$$$$$$$$$$$$$$")
#     df = data.pd()
#     print(df[:2])
#     if df.empty:
#         print('Empty Dataframe')  ## do nothing
#     else:
#         df.rename(columns={'o':'open', 'h':'high', 'l':'low', 'c':'close', 'v':'volume'}, inplace=True, errors='raise')
#     return df

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
#     dict = data.pd()
#     dict['bsize'] = int(dict['bsize'])
#     dict['asize'] = int(dict['asize'])
#     dict['time']  = dict.pop('timestamp')
#     dict['time']  = pd.to_datetime(dict['time'].decode("utf-8"))
#     dict['sym']   = dict['sym'].decode("utf-8")
#     return dict

# def ohlcv_agg_old(data):
#     df = data.pd()
#     # create datetime column
#     df['time'] = df['time'].dt.floor('min')
#     # group by sym and datetime, and aggregate
#     agg = {
#         'price': ['first', 'max', 'min', 'last'],
#         'size': 'sum'
#     }
#     ohlcv = df.groupby(['sym', 'time']).agg(agg)
#     # rename columns to match KDB/Q query
#     ohlcv.columns = ['open', 'high', 'low', 'close', 'volume']
#     # reset index to make columns sym and datetime
#     ohlcv = ohlcv.reset_index()[['sym', 'time', 'open', 'high', 'low', 'close', 'volume']]
#     ohlcv = ohlcv.astype({'open':'float', 'high':'float','low':'float','close':'float','volume':'int64'})
#     # print(ohlcv)
#     return ohlcv


# def vwap_agg_old(data):
#     print(kx.q.meta(data))
#     df = data.pd()

#     if df.empty:
#         # print('Empty Dataframe')
#         vwap = df
#     else:
#         # create datetime column
#         df['time'] = df['time'].dt.floor('min')

#         # group by sym and datetime, and calculate VWAP and accumulated volume
#         vwap = df.groupby(['sym', 'time']).apply(lambda x: pd.Series({
#             'vwap': (x['price'] * x['size']).sum() / x['size'].sum(),
#             'accVol': x['size'].sum()
#         }))
#         vwap = vwap.reset_index()[['sym', 'time', 'vwap', 'accVol']]
#         vwap = vwap.astype({'vwap':'float', 'accVol':'int64'})
#         print(vwap)
#     return vwap