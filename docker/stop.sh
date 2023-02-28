#!/bin/bash

echo 'Stopping RT...'
docker-compose -f 'docker-compose-rt.yaml' down --remove-orphans