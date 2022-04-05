# kxi-microservices-data-services

## Create data folders 
```bash
$ cd kxi-microservices-data-services
$ mkdir db tplog cache
$ chmod 777 db tplog cache
```


## Docker start
```bash
$ docker login registry.dl.kx.com
$ ./prepEnv.sh
$ source .env
$ docker-compose up -d
$ docker-compose logs -f 
```

## Authentication
```bash
## create file and populate appropriately
$ tee .cloud_auth_env << EOF
export AWS_REGION=
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AZURE_STORAGE_ACCOUNT=
export AZURE_STORAGE_SHARED_KEY=
export GOOGLE_TOKEN=
export GCLOUD_PROJECT_ID=
EOF
```

## Publish data
```q
// open handle 
q)tp:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-tp-1"

// publish data
q)tp(`upd;`quote;(10#.z.N;10?`IBM`AAPL`GOOG;10#.z.p;10?1000f;10?1000f;10?1000;10?1000))
q)tp(`upd;`trade;(10#.z.N;10?`IBM`AAPL`GOOG;10#.z.p;10?1000f;10?1000))
q)tp(`upd;`quote;flip (10?`IBM`AAPL`GOOG;10#.z.p;10?1000f;10?1000f;10?1000f;10?1000f))
q)tp(`upd;`xref;(10#.z.p;10?`IBM`AAPL`GOOG;10?10;10?0Ng;10?10h;10?10;10?1000)) 
```


## Fix Purview 
```q
q)sgrc:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-sgrc-1"
q)sgrc"update startTS:-0Wp, endTS:first `timestamp$(exec max prtns[;`max_date] from .sgrc.i.daps where instance = `HDB) from `.sgrc.i.daps where instance = `HDB"
`.sgrc.i.daps
q)sgrc"update startTS:(exec max endTS from .sgrc.i.daps where not endTS=0Wp) from `.sgrc.i.daps where instance = `RDB"
`.sgrc.i.daps
```


## Query Data
```q
q)gw:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-sggw-1"
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`quote;"p"$.z.d-1;"p"$.z.d+1);`f;(0#`)!())
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`quote;"p"$.z.d-1;"p"$.z.d+1);`f;(0#`)!())
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`trade;"p"$2014.11.22-1;"p"$2014.11.22+1);`f;(0#`)!())
```

## Custom API
```q
q)gw(`.custom.countBy;(`table`startTS`endTS`byCols)!(`quote;"p"$.z.d-1;"p"$.z.d+1;`bidPrice);`f;(0#`)!())
```


```bash
curl -X POST --header "Content-Type: application/json"\
 --header "Accepted: application/json"    \
 --data '{ "table":  "quote", "startTS":"2022.02.10D00:00:00.000", "endTS":"2023.02.12D00:00:00.000"}'\
  `docker port kxi-microservices-data-services-sggw-1 | grep 8080 | cut -f3 -d " "`"/kxi/getData"
```
