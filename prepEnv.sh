#!/bin/bash
source .env
source .cloud_auth_env 
eval "echo \"$(cat cfg/assembly_sample.yaml)\"" > cfg/resolved_assembly_sample.yaml
