#!/bin/bash
set -eu
SCALE=3
RUNID=$(uuidgen)
echo "RunId,Date/Time,Container,RAM Max Usage (GiB)"
for CONTAINER in $(docker ps --format '{{.Names}}'); do
    DATETIME=$(date '+%Y-%m-%d %H:%M:%S')
    if [[ "$(docker exec -it $CONTAINER stat -fc %T /sys/fs/cgroup/)" != "cgroup2fs" ]]; then
        MAX_RAM_CGROUP="/sys/fs/cgroup/memory/memory.max_usage_in_bytes"
    else
        MAX_RAM_CGROUP="/sys/fs/cgroup/memory.peak"
    fi
    RAM_MAX_USAGE_B="$(docker exec -it $CONTAINER cat $MAX_RAM_CGROUP | tr -d '\r')"
    RAM_MAX_USAGE_MiB=$(bc <<< "scale=$SCALE;($RAM_MAX_USAGE_B/(1024 * 1024))")
    RAM_MAX_USAGE_GiB=$(bc <<< "scale=$SCALE;($RAM_MAX_USAGE_MiB/1024)")
    echo "$RUNID,$DATETIME,$CONTAINER,$RAM_MAX_USAGE_GiB"
done