# Kubernetes

## Pre-reqs
* EKS Cluster Rook Ceph, Autoscaler provisioned
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

```bash
$ kubectl apply -f rook-ceph-pvc.yaml -n kdb
$ kubectl apply -f microservices-assembly.yaml -n kdb
```


```bash
$ kubectl delete -f microservices-assembly.yaml -n kdb
```
### ceph-toolbox
* https://rook.github.io/docs/rook/v1.5/ceph-toolbox.html
