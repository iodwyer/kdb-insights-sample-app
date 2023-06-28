docker compose -f docker-compose-rt.yaml down --remove-orphans

docker volume rm $(docker volume ls -qf dangling=true)

source rt-env.env && docker compose -f docker-compose-rt.yaml up -d 

docker logs docker-sm > kx.log
docker logs sm-single > kx.log

docker logs docker-da-single-1 > kx.log


mkdir rt-data-0 publisher-1 sm-logs da-logs subscriber-1 data rt-data-session sp

sudo rm -rf rt-data-0 publisher-1 sm-logs da-logs subscriber-1 data rt-data-session sp

chmod -R 777 rt-data-0 publisher-1 sm-logs da-logs subscriber-1 data rt-data-session sp