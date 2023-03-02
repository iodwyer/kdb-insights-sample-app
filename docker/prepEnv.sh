#!/bin/bash

source .env

eval "echo \"$(cat cfg/prep_assembly.yaml)\"" > cfg/assembly.yaml

echo "${mnt_dir}"
