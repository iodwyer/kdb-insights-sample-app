
# Docker 

## Create data folders 
```bash
$ mkdir -p data tplog sp/checkpoints
$ sudo chmod 777 -R data tplog sp
```

## KX License
Copy obtained KX License into the `.qp.licenses` folder in your `$HOME` directory. Further info here: https://code.kx.com/insights/core/qpacker/qpacker.html#licenses
```bash
$ mkdir $HOME/.qp.licenses
$ cp k[4,c,x].lic $HOME/.qp.licenses
```

## Docker start
```bash
$ docker login registry.dl.kx.com          ## enter obtained credentials
$ docker-compose up -d
$ docker-compose logs -f 
```


## Query Data
### Q
```q
// getData API
q)gw:hopen "J"$last ":" vs first system"docker port docker-sggw-1"
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`quote;"p"$.z.d-1;"p"$.z.d+1);`f;(0#`)!())
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`trade;"p"$.z.d;.z.p);`f;(0#`)!())

// Custom API
q)gw(`.custom.countBy;(`table`startTS`endTS`byCols)!(`trade;"p"$.z.d-1;"p"$.z.d+1;`size);`f;(0#`)!())

// SQL API
q)gw(`.kxi.sql;enlist[`query]!enlist"SELECT * FROM trade WHERE (date between '2022.12.19' and '2022.12.20') and (sym = 'AAPL')";`f;(0#`)!())
  
// getMeta API
q)args:`region`startTS`endTS!(`nyc;-0Wp;0Wp)
q)gw(`.kxi.getMeta;args;`;(0#`)!())
```

### Python
```python
import pykx as kx
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pytz

gw = kx.QConnection(host='localhost', port=5040, no_ctx = True)                        ## SG Gateway port

## getData
START_TIME = datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(minutes = 36000)   ## 15 Mins ago
END_TIME = datetime.datetime.now(tz=pytz.utc)                                           ## Now

empty_dict = {'':''}

get_data_query_params = {
    'table': 'trade',
    'startTS': START_TIME,
    'endTS': END_TIME
}

tab = gw(kx.SymbolAtom('.kxi.getData'), get_data_query_params, 'f', empty_dict)
data = tab[1].pd()

print(data)

plt.plot(data.size)
plt.show()


## SQL
sql_query_params = {
    'query': b"SELECT * FROM trade WHERE (date between '2022.12.19' and '2022.12.20') and (sym = 'AAPL')" 
}

tab = gw(kx.SymbolAtom('.kxi.sql'), sql_query_params, 'f', empty_dict)
data = tab[1].pd()
```
### Curl
```bash
curl -X POST --header "Content-Type: application/json"\
 --header "Accepted: application/json"    \
 --data '{ "table":  "trade", "startTS":"2022.02.10D00:00:00.000", "endTS":"2022.02.12D00:00:00.000"}'\
  `docker port docker-sggw-1 | grep 8080 | cut -f3 -d " "`"/kxi/getData"
```
