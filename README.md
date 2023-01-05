# kxi-microservices-data-services
- [kxi-microservices-data-services](#kxi-microservices-data-services)
  - [Architecture](#architecture)
  - [Quick Links](#quick-links)
    - [Storage Manager](#storage-manager)
    - [Data Access](#data-access)
    - [Service Gateway](#service-gateway)
    - [Stream Processor](#stream-processor)
  - [Authentication](#authentication)
  - [Create data folders](#create-data-folders)
  - [Docker start](#docker-start)
  - [Query Data](#query-data)

## Architecture
![Architecture](img/arch_diagram.png)

## Quick Links
<https://code.kx.com/insights/microservices/intro.html>

### Storage Manager
* <https://code.kx.com/insights/microservices/storage-manager/introduction.html>

### Data Access
* <https://code.kx.com/insights/microservices/data-access/introduction.html>

### Service Gateway
* <https://code.kx.com/insights/microservices/data-access/introduction_sg.html>

### Stream Processor
* <https://code.kx.com/insights/microservices/stream-processor/index.html>


## Authentication
```bash
## create file and populate appropriately
$ tee .cloud_auth_env << EOF
AWS_REGION=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AZURE_STORAGE_ACCOUNT=
AZURE_STORAGE_SHARED_KEY=
GOOGLE_TOKEN=
GCLOUD_PROJECT_ID=
EOF
```

## Create data folders 
```bash
$ cd kxi-microservices-data-services
$ mkdir -p data tplog sp/checkpoints
$ sudo chmod 777 -R data tplog sp
```

## Docker start
```bash
$ docker login registry.dl.kx.com
$ docker-compose up -d
$ docker-compose logs -f 
```


## Query Data
```q
q)gw:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-sggw-1"
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`quote;"p"$.z.d-1;"p"$.z.d+1);`f;(0#`)!())
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`trade;"p"$.z.d;.z.p);`f;(0#`)!())
```
```bash
curl -X POST --header "Content-Type: application/json"\
 --header "Accepted: application/json"    \
 --data '{ "table":  "trade", "startTS":"2022.02.10D00:00:00.000", "endTS":"2022.02.12D00:00:00.000"}'\
  `docker port kxi-microservices-data-services-sggw-1 | grep 8080 | cut -f3 -d " "`"/kxi/getData"
```
```
## Custom API
```q
q)gw(`.custom.countBy;(`table`startTS`endTS`byCols)!(`trade;"p"$.z.d-1;"p"$.z.d+1;`size);`f;(0#`)!())
```