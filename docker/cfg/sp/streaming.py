from kxi import sp
import pykx as kx

kfk_broker  = 'kafka.trykdb.kx.com:443'
kfk_broker_options = {
    'sasl.username': 'demo',
    'sasl.password': 'demo',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'security.protocol': 'SASL_SSL'
    }

trade_schema_types = {
    'time':     kx.TimestampAtom,
    'sym':      kx.SymbolAtom,
    'price':    kx.FloatAtom,
    'size':     kx.LongAtom
    }

def transform_dict_to_table(d):     ## transform dictionary to table object
    return kx.q.enlist(d)   

subscriber_pipe = (sp.read.from_kafka(topic='trade', brokers=kfk_broker, options=kfk_broker_options)
    | sp.decode.json()    
    | sp.map(transform_dict_to_table, name = 'transform trade')
    | sp.transform.rename_columns({'timestamp': 'time'})            ## rename incoming column 'timestamp' to 'time' 
    | sp.transform.schema(trade_schema_types)
    | sp.write.to_subscriber(table='data', key_col=[], name='grafana-subscriber', publishFrequency=500, cache_limit=100)
    )

sp.run(subscriber_pipe)