
# Docker 
## Pre-reqs
* [Install docker](https://docs.docker.com/engine/install/)
* [Run docker commands without `sudo`](https://docs.docker.com/engine/install/linux-postinstall/)
## Create data folders 
```bash
$ mkdir -p data/sp/checkpoints tplog lic
$ sudo chmod 777 -R data tplog
```

## KX License
Copy obtained KX License into the `lic` folder. Further info here: https://code.kx.com/insights/core/qpacker/qpacker.html#licenses
<!-- install -D file.txt /path/to/non/existing/dir/file.txt  -->
```bash
$ cp /path/to/k[4,c,x].lic lic/
```

## Docker start
Log in to the [KX download portal](https://portal.dl.kx.com) and obtain a bearer token. 
```bash
$ docker login -u iodwyer@kx.com -p $BEARER portal.dl.kx.com         ## enter obtained credentials
$ docker compose up -d
$ docker compose logs -f 
```

## Query Data
### q
```q
// getData API
q)gw:hopen `:localhost:5040
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`quote;"p"$.z.d-1;"p"$.z.d+1);`;(0#`)!())
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`trade;"p"$.z.d;.z.p);`;(0#`)!())

// Custom API
q)gw(`.custom.simple;(`table`ticker`startTS`endTS)!(`trade;`AAPL;"p"$.z.d-1;"p"$.z.d+1);`;(0#`)!())

// SQL API
q)gw(`.kxi.sql;enlist[`query]!enlist"SELECT * FROM trade WHERE (date between '2022.12.19' and '2022.12.20') and (sym = 'AAPL')";`;(0#`)!())
  
// getMeta API
q)args:`region`startTS`endTS!(`nyc;-0Wp;0Wp)
q)gw(`.kxi.getMeta;args;`;(0#`)!())
```

### Python
```python
iimport pykx as kx
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pytz
import random
import requests
from bs4 import BeautifulSoup

def get_company_name(ticker):
    print('Querying for ticker info: ' + ticker)
    url = f'https://finance.yahoo.com/quote/{ticker}'
    headers = {'User-Agent': 'Mozilla/5.0'}  # Avoid blocking
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # The title tag contains company name and ticker
    title = soup.title.string
    
    if ticker in title:
        ticker = '(' + ticker + ')'
        name = title.split(ticker)[0]
        return(name + ticker)
    return 'Name not found'

gw = kx.QConnection(host='localhost', port=5040, no_ctx = True)                        ## SG Gateway port


## SQL
sql_query_params = {
    'query': b"SELECT * FROM trade WHERE (date between '2022.12.19' and '2022.12.20') and (sym = 'AAPL')" 
}

empty_dict = {'':''}

tab = gw(kx.SymbolAtom('.kxi.sql'), sql_query_params, '', empty_dict)
data = tab[1].pd()


## getData
START_TIME = datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(minutes = 36000)   ## 15 Mins ago
END_TIME = datetime.datetime.now(tz=pytz.utc)                                           ## Now

get_data_query_params = {
    'table': 'trade',
    'startTS': START_TIME,
    'endTS': END_TIME
}

tab = gw(kx.SymbolAtom('.kxi.getData'), get_data_query_params, '', empty_dict)
df = tab[1].pd()

unique_syms = list(set(df['sym']))
selected_sym = random.choice(unique_syms)
company_name = get_company_name(selected_sym)

filtered_df = df[df['sym'] == selected_sym]

plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Trade Data - ' + company_name)
plt.xticks(rotation=45)
plt.tight_layout()

plt.plot(filtered_df['time'], filtered_df['price'], label='Price')
plt.show()
```
### Curl
```bash
start_time=$(date +"%Y.%m.%dD00:00:00.000") 
end_time=$(date +"%Y.%m.%dD%T.000")
curl -X POST --header "Content-Type: application/json" \
    --header "Accepted: application/json" \
    --data "{\"table\": \"trade\", \"startTS\": \"${start_time}\", \"endTS\": \"${end_time}\"}" \
    http://localhost:8080/kxi/getData
```


## Custom APIs

When creating custom analytics that access data there is a helper function `.kxi.selectTable` which understands the data model within each DAP and can help select from the tables necessary to return the appropriate records. It's interface is as follows:

| name | type | description |
|------|-----|----------------|
| tn   | symbol | Name of table to retrieve data from |
| ts   | timestamp[2] | Time period of interest |
| wc   | list[] | Where clause of what to select | 
| bc   | dict/boolean | By clause for select |
| cn   | symbol | Names of columns to select for. Include any columns needed in aggregations |
| agg  | dict | Select clause/aggregations to apply to table |