source rt-env.env && docker compose -f docker-compose-rt.yaml down --remove-orphans

sudo rm -rf rt-data-0 publisher-1 sm-logs da-logs subscriber-1 data rt-data-session sp tplog
ls -alrth 

mkdir rt-data-0 publisher-1 sm-logs da-logs subscriber-1 data rt-data-session sp tplog

ls -larth 

chmod -R 777 rt-data-0 publisher-1 sm-logs da-logs subscriber-1 data rt-data-session sp tplog

source rt-env.env && docker compose -f docker-compose-rt.yaml up -d 




