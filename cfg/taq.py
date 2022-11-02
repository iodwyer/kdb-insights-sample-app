from kxi import sp

quote_schema = {
    'timestamp': 'timestamp',
    'sym': 'symbol',
    'bid': 'float',
    'ask': 'float',
    'bsize': 'long',
    'asize': 'long'
}

quote = (sp.read.from_kafka(topic='quote', brokers='104.198.219.51:9091')
    | sp.decode.json()
    | sp.map('{[data] "PS**jj"$data }')
    | sp.map(lambda x: ('quote', x))
    | sp.write.to_process(handle=':tp:5010', mode='function', target='.u.updSP'))

# trade = (sp.read.from_kafka(topic='trade', brokers='104.198.219.51:9091')
#     | sp.decode.json()
#     | sp.transform.schema(quote_schema)
#     | sp.write.to_console())

sp.run(quote)