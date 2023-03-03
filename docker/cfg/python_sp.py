from kxi import sp
import pykx as kx
import datetime
import pandas as pd
import numpy as np

# ohlcv_stream: .qsp.read.fromCallback[`ohlcv]
#   .qsp.window.tumbling[00:00:10; `time; .qsp.use ``sort!11b]
#   .qsp.map[ { (`ohlcv;value flip 0!select open:first price, high:max price, low:min price, close:last price, volume:sum size by sym, exchange, time:(`date$time) + time.minute from x) }]
#   .qsp.write.toProcess[.qsp.use `handle`target`spread!(`$raze ":",(.Q.opt[.z.x] `ip_address),":",(.Q.opt[.z.x] `tp_port);`.u.upd;1b)]
#   / .qsp.write.toConsole[]


# vwap_stream: .qsp.read.fromCallback[`vwap]
#   .qsp.window.tumbling[00:00:10; `time; .qsp.use ``sort!11b]  // 10 second for debugging
#   .qsp.map[ { (`vwap;value flip 0!select vwap:size wavg price, accVol:sum size by sym, exchange, time:(`date$time) + time.minute from x) }]
#   .qsp.write.toProcess[.qsp.use `handle`target`spread!(`$raze ":",(.Q.opt[.z.x] `ip_address),":",(.Q.opt[.z.x] `tp_port);`.u.upd;1b)]
#   / .qsp.write.toConsole[]

def func(data):
    df = data.pd()
    # create datetime column
    # df['time'] = df['date'] + df['time'].dt.floor('min')
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
    tab = kx.toq.from_pandas_dataframe(ohlcv)
    return tab

ohlcv_pipeline = (sp.read.from_stream(table='trade',stream="data", prefix="rt-")
    | sp.window.tumbling(period = datetime.timedelta(seconds = 10), time_column = 'time', sort=True)
    | sp.map(func)
    # | sp.write.to_console())
    | sp.write.to_stream(table='ohlcv',stream="data", prefix="rt-"))

# vwap_pipeline = (sp.read.from_stream(table='trade',stream="data", prefix="rt-")
#     # | sp.decode.json()
#     # | sp.map('{[data] (enlist[`timestamp]!enlist `time) xcol enlist "PS*j"$data }')
#     # | sp.map(lambda x: ('trade', x))
#     | sp.window.tumbling(period = datetime.timedelta(seconds = 10), time_column = 'time', sort=True)
#     | sp.map(func)
#     # | sp.write.to_console())
#     | sp.write.to_console())

# sp.run(ohlcv_pipeline, vwap_pipeline)
sp.run(ohlcv_pipeline)