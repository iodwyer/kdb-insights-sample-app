#!/bin/bash

# Evaluate the assembly file (for mnt_dir specifically)
./prepEnv.sh

docker-compose -f 'docker-compose-rt.yaml' --env-file .env up -d