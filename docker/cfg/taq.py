from kxi import sp

# tp_hostport = ':tp:5010'
tp_hostport = '127.0.0.1:5001'
kfk_broker  = '104.198.219.51:9091'

trade_schema = {
    'timestamp':  'timestamp',
    'sym':        'symbol',
    'price':      'float',
    'size':       'long'
}

quote_schema = {
    'timestamp':  'timestamp',
    'sym':        'symbol',
    'bid':        'float',
    'ask':        'float',
    'bsize':      'long',
    'asize':      'long'
}

trade_pipeline = (sp.read.from_kafka(topic='trade', brokers=kfk_broker)
    | sp.decode.json()
    | sp.map('{[data] (enlist[`timestamp]!enlist `time) xcol enlist "PS*j"$data }')
    # | sp.map(lambda x: ('trade', x))
    # | sp.write.to_console())
    | sp.write.to_stream(table='trade',stream="data", prefix="rt-"))


quote_pipeline = (sp.read.from_kafka(topic='quote', brokers=kfk_broker)
    | sp.decode.json()
    | sp.map('{[data] (enlist[`timestamp]!enlist `time) xcol enlist "PS**jj"$data }')
    # | sp.map(lambda x: ('quote', x))
    | sp.write.to_stream(table='quote',stream="data", prefix="rt-"))

sp.run(trade_pipeline, quote_pipeline)