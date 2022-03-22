#!/bin/bash
source .env
chmod +x db
eval "echo \"$(cat cfg/assembly_sample.yaml)\"" > cfg/resolved_assembly_sample.yaml