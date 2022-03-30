#!/bin/bash
source .env
source .aws_env 
eval "echo \"$(cat cfg/assembly_sample.yaml)\"" > cfg/resolved_assembly_sample.yaml