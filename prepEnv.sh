#!/bin/bash
source .env
chmod o+rw db
eval "echo \"$(cat cfg/assembly_sample.yaml)\"" > cfg/resolved_assembly_sample.yaml