#!/bin/bash
source .env
source .aws_env 
mkdir db tplog
sudo chmod 777 db tplog 
eval "echo \"$(cat cfg/assembly_sample.yaml)\"" > cfg/resolved_assembly_sample.yaml