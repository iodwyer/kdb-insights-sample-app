import pykx as kx
import datetime
import pytz

gw = kx.QConnection(host='localhost', port=49164, no_ctx = True)                    ## SG Gateway port
# gw = kx.QConnection(host='localhost', port=5555, no_ctx = True)
# gw = kx.q('hopen 49164')

START_TIME = datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(minutes = 36000)  ## 15 Mins ago
END_TIME = datetime.datetime.now(tz=pytz.utc)                                       ## Now

query_params = {
    'table': 'trade',
    'startTS': START_TIME,
    'endTS': END_TIME
}

empty_dict = {'':''}

tab = gw(kx.SymbolAtom('.kxi.getData'), query_params, 'f', empty_dict)

data = tab[1].pd()

print(data)