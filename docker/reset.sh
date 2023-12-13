
docker compose -f docker-compose-rt.yaml down --remove-orphans
docker compose down --remove-orphans

FOLDERS="rt-log sm-logs da-logs data rt-session sp"

sudo rm -rf $FOLDERS
ls -alrth 

mkdir $FOLDERS

ls -larth 

chmod -R 777 $FOLDERS

docker compose up -d 