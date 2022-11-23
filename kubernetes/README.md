# kubernetes

## Pre-reqs
* EKS Cluster with ~~AWS Load Balancer~~ , Rook Ceph, Autoscaler provisioned
* `kubectl` CLI


## Set-up
```bash
## create and set default namespace
$ kubectl create namespace kdb
$ sed -i 's|default.svc|kdb.svc|g' microservices-assembly.yaml
$ kubectl config set-context --current --namespace=kdb
```

```bash
## don't forget AWS REGION
# $ kubectl create configmap kxinsights-s3-configmap \
#     --from-file=sym=db/sym \
#     --from-file=par.txt=db/par.txt
```

```bash
$ kubectl create secret docker-registry kx-repo-access \
    --docker-username=${NEXUS_USER} \
    --docker-password=${NEXUS_PASSWORD} \
    --docker-server=registry.dl.kx.com
```

```bash
$ kubectl create secret generic kdb-license-info \
    --from-literal=license=$(base64 -w 0 < $QLIC/kc.lic)
```

```bash
$ kubectl create secret generic aws-access-secret \
    --from-literal=AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    --from-literal=AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
```    


## To do 
* Add service discovery microservice (remove need for `sed` command)
* add historic data to s3 bucket + add s3 tier to SM
* consider autoscaling DAP's + Agg procs based on CPU
* consider autoscaling on number of queries in the queue (RC? or GW?)
* authentication (add layer in front of GW? Link to SAML; Active Directory?)
* provision different PVC's for SP/DAP etc
* Add RT microservice