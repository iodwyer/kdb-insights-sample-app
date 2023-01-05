
# Docker 

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
### Q
```q
## getData
q)gw:hopen "J"$last ":" vs first system"docker port kxi-microservices-data-services-sggw-1"
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`quote;"p"$.z.d-1;"p"$.z.d+1);`f;(0#`)!())
q)gw(`.kxi.getData;(`table`startTS`endTS)!(`trade;"p"$.z.d;.z.p);`f;(0#`)!())
```

```q
## Custom API
q)gw(`.custom.countBy;(`table`startTS`endTS`byCols)!(`trade;"p"$.z.d-1;"p"$.z.d+1;`size);`f;(0#`)!())
```

### Curl
```bash
curl -X POST --header "Content-Type: application/json"\
 --header "Accepted: application/json"    \
 --data '{ "table":  "trade", "startTS":"2022.02.10D00:00:00.000", "endTS":"2022.02.12D00:00:00.000"}'\
  `docker port kxi-microservices-data-services-sggw-1 | grep 8080 | cut -f3 -d " "`"/kxi/getData"
```