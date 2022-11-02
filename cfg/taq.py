from kxi import sp

tp_hostport = ':tp:5010'
kfk_broker = '104.198.219.51:9091'

trade_schema = {
    'timestamp': 'timestamp',
    'sym': 'symbol',
    'price': 'float',
    'size': 'long'
}

quote_schema = {
    'timestamp': 'timestamp',
    'sym': 'symbol',
    'bid': 'float',
    'ask': 'float',
    'bsize': 'long',
    'asize': 'long'
}

trade = (sp.read.from_kafka(topic='trade', brokers=kfk_broker)
    | sp.decode.json()
    | sp.map('{[data] "PS*j"$data }')
    | sp.map(lambda x: ('trade', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.updSP'))

quote = (sp.read.from_kafka(topic='quote', brokers=kfk_broker)
    | sp.decode.json()
    | sp.map('{[data] "PS**jj"$data }')
    | sp.map(lambda x: ('quote', x))
    | sp.write.to_process(handle=tp_hostport, mode='function', target='.u.updSP'))

sp.run(quote, trade)