
docker compose -f docker-compose-rt.yaml down --remove-orphans

FOLDERS="rt-log sp-log sm-logs da-logs data rt-session sp"

sudo rm -rf $FOLDERS
ls -alrth 

mkdir $FOLDERS

ls -larth 

chmod -R 777 $FOLDERS

docker compose -f docker-compose-rt.yaml up -d 