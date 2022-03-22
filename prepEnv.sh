#!/bin/bash
source .env
mkdir db tplog
chmod o+rw db tplog 
eval "echo \"$(cat cfg/assembly_sample.yaml)\"" > cfg/resolved_assembly_sample.yaml