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
$ docker-compose up
```


## Publish data
```q
tp:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-tp-1"
tp(`.u.upd;`quote;(10#.z.N;10?`IBM`AAPL`GOOG;10#.z.p;10?1000f;10?1000f;10?1000;10?1000))
tp(`.u.upd;`trade;(10#.z.N;10?`IBM`AAPL`GOOG;10#.z.p;10?1000f;10?1000))
tp(`.u.upd;`xref;(10#.z.p;10?`IBM`AAPL`GOOG;10?10;10?0Ng;10?10h;10?10;10?1000)) 
```


## Query Data
```q
gw:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-sggw-1"
gw(`.kxi.getData;(`table`startTS`endTS)!(`quote;"p"$.z.d-1;"p"$.z.d+1);`f;(0#`)!())
gw(`.kxi.getData;(`table`startTS`endTS)!(`xref;"p"$.z.d-1;"p"$.z.d+1);`f;(0#`)!())
```

```bash
curl -X POST --header "Content-Type: application/json"\
 --header "Accepted: application/json"    \
 --data '{ "table":  "quote", "startTS":"2022.02.10D00:00:00.000", "endTS":"2023.02.12D00:00:00.000"}'\
  `docker port kxi-microservices-data-services-sggw-1 | grep 8080 | cut -f3 -d " "`"/kxi/getData"
```
