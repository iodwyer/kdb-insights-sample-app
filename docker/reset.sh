
docker compose -f docker-compose-rt.yaml down --remove-orphans

FOLDERS="rt-data-0 sp-log sm-logs da-logs data rt-data-session sp"


sudo rm -rf $FOLDERS
ls -alrth 

mkdir $FOLDERS

ls -larth 

chmod -R 777 $FOLDERS

docker compose -f docker-compose-rt.yaml up -d 