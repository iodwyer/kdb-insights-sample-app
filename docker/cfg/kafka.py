from kxi import sp

trade_source = (sp.read.from_kafka(topic = 'subway', brokers = '34.130.174.118:9091')
    | sp.decode.json()
    | sp.write.to_console())

sp.run(trade_source)