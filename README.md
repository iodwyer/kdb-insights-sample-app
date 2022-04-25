# kxi-microservices-data-services
- [kxi-microservices-data-services](#kxi-microservices-data-services)
  - [Quick Links](#quick-links)
    - [Storage Manager](#storage-manager)
    - [Data Access](#data-access)
    - [Service Gateway](#service-gateway)
  - [Authentication](#authentication)
  - [Create data folders](#create-data-folders)
  - [Docker start](#docker-start)
  - [Publish data](#publish-data)
  - [Fix Purview](#fix-purview)
  - [Query Data](#query-data)
  - [Custom API](#custom-api)
## Quick Links

<https://code.kx.com/insights/microservices/intro.html>

### Storage Manager

* <https://code.kx.com/insights/microservices/storage-manager/introduction.html>
* <https://code.kx.com/insights/microservices/artefacts.html#storage-manager>

### Data Access

* <https://code.kx.com/insights/microservices/data-access/introduction.html>
* <https://code.kx.com/insights/microservices/artefacts.html#data-access>

### Service Gateway

* <https://code.kx.com/insights/microservices/data-access/introduction_sg.html>
* <https://code.kx.com/insights/microservices/artefacts.html#service-gateway>

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

## Create data folders 
```bash
$ cd kxi-microservices-data-services
$ mkdir -p db/hdb/data tplog cache
$ cp cfg/sym db/hdb/data
$ sudo chown -R nobody:nogroup db tplog cache
$ sudo chmod 777 -R db tplog cache
```


## Docker start
```bash
$ docker login registry.dl.kx.com
$ ./prepEnv.sh
$ source .env
$ source .cloud_auth_env
$ docker-compose up -d
$ docker-compose logs -f 
```



## Publish data
```q
// open handle 
q)tp:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services_tp_1"

// publish data
q)tp(`upd;`quote;flip (10?`IBM`AAPL`GOOG;10#.z.p;10?1000f;10?1000f;10?1000f;10?1000f))
q)tp(`upd;`trade;flip (10?`IBM`AAPL`GOOG;10#.z.p;10?`buy`sell;10?100j;10?1000f;10?`in`out;10?0ng;10?1000j;10?1000f;10?1000f))
// q)tp(`upd;`xref;(10#.z.p;10?`IBM`AAPL`GOOG;10?10;10?0Ng;10?10h;10?10;10?1000)) 
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
q)gw:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services_sggw_1"
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`quote;"p"$.z.d-1;"p"$.z.d+1);`f;(0#`)!())
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`trade;"p"$2014.11.22-1;"p"$2014.11.22+1);`f;(0#`)!())
```
```bash
curl -X POST --header "Content-Type: application/json"\
 --header "Accepted: application/json"    \
 --data '{ "table":  "quote", "startTS":"2022.02.10D00:00:00.000", "endTS":"2023.02.12D00:00:00.000"}'\
  `docker port kxi-microservices-data-services-sggw-1 | grep 8080 | cut -f3 -d " "`"/kxi/getData"
```

## Custom API
```q
q)gw(`.custom.countBy;(`table`startTS`endTS`byCols)!(`quote;"p"$.z.d-1;"p"$.z.d+1;`bidPrice);`f;(0#`)!())
```