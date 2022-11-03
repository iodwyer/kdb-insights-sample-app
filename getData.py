import pykx as kx
import datetime
import pytz

gw = kx.QConnection(host='localhost', port=49164)
# gw = kx.q('hopen 49164')

START_TIME = datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(minutes = 15)  ## 15 Mins ago
END_TIME = datetime.datetime.now(tz=pytz.utc)                                       ## Now

query_params = {
    'table': 'trade',
    'startTS': START_TIME,
    'endTS': END_TIME
}

empty_dict = {'':''}

tab = gw('.kxi.getData', query_params, 'f', empty_dict).pd()

print(tab)