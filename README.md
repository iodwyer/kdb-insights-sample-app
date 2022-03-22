# kxi-microservices-data-services

## Docker start
```bash
$ cd kxi-microservices-data-services
$ ./prepEnv
$ source .env
$ docker-compose up
```


## Publish data
```q
tp:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-tp-1"
tp(`.u.upd;`quote;(10#.z.N;10?`IBM`AAPL`GOOG;10#.z.p;10?1000f;10?1000f;10?1000;10?1000))
```

## Query Data
```q
gw:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-sggw-1"
gw(`.kxi.getData;(`table`startTS`endTS)!(`quote;"p"$.z.d-1;"p"$.z.d+1);`f;(0#`)!())
```