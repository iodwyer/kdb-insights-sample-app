from kxi import sp

kfk_broker  = '34.130.174.118:9091'

trade_source = (sp.read.from_kafka(topic='subway', brokers=kfk_broker)
    | sp.decode.json()
    | sp.write.to_console())

sp.run(trade_source)