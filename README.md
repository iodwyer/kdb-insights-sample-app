# kxi-microservices-data-services

## Create data folders 
```bash
$ cd kxi-microservices-data-services
$ mkdir db tplog
$ chmod o+rw db tplog 
```


## Docker start
```bash
$ ./prepEnv.sh
$ source .env
$ docker-compose up -d
$ docker-compose logs -f 
```


## Publish data
```q
q)tp:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-tp-1"
q)tp(`.u.upd;`quote;(10#.z.N;10?`IBM`AAPL`GOOG;10#.z.p;10?1000f;10?1000f;10?1000;10?1000))
q)tp(`.u.upd;`trade;(10#.z.N;10?`IBM`AAPL`GOOG;10#.z.p;10?1000f;10?1000))
q)tp(`.u.upd;`xref;(10#.z.p;10?`IBM`AAPL`GOOG;10?10;10?0Ng;10?10h;10?10;10?1000)) 
```


## Fix Purview 
```q
q)sgrc:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-sgrc-1"
q)sgrc"update startTS:-0Wp from `.sgrc.i.daps where instance = `HDB"
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

```bash
curl -X POST --header "Content-Type: application/json"\
 --header "Accepted: application/json"    \
 --data '{ "table":  "quote", "startTS":"2022.02.10D00:00:00.000", "endTS":"2023.02.12D00:00:00.000"}'\
  `docker port kxi-microservices-data-services-sggw-1 | grep 8080 | cut -f3 -d " "`"/kxi/getData"
```
