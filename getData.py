import pykx as kx
import datetime
import pytz

gw = kx.QConnection(host='localhost', port=5001)

START_TIME = (datetime.datetime.now(tz=pytz.utz) - datetime.timedelta(minutes = 15)).strftime("%Y.%m.%dD%H:%M:%S")  ## 15 Mins ago
END_TIME = datetime.datetime.now(tz=pytz.utc).strftime("%Y.%m.%dD%H:%M:%S")  ## Now

query_params = {
    'table': 'trade',
    'startTS': START_TIME,
    'endTS': END_TIME
}

empty_dict = {'':''}

tab = gw('.kxi.getData', query_params, 'f', empty_dict).pd()

print(tab)
# gw('.kxi.getData', pytab, ['col1'], 1).pd()

