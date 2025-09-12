# kxi-auth
https://code.kx.com/insights/1.14/microservices/database/configuration/advanced/custom-auth-ipc.html

## Create self signed keystore 
``` 
$ mkdir keystore && cd keystore
```

```
$ keytool -genkeypair \
  -alias testkey \
  -keyalg RSA \
  -keystore keystore.p12 \
  -storetype PKCS12 \
  -storepass changeit \
  -validity 365 \
  -keysize 2048 \
  -dname "CN=localhost, OU=Dev, O=Test, L=City, ST=State, C=US"
```


Create plaintext password 
```
$ echo -n "changeit" > keystore.pkcs12
```

### Docker compose setup 

Add the following to your kxi-gw (java gateway container)
```bash
      - GATEWAY_EXT_QIPC_PORT=5051
      - KXI_SG_AUTH_IPC_HOST=kxi-auth
      - KXI_SG_AUTH_IPC_PORT=5000
      - KXI_SG_AUTH_IPC_AUTH_API=authorize
      - KXI_SG_KEYSTORE=/keystore/keystore.p12
      - KXI_SG_KEYSTORE_PASS_FILE=/keystore/keystore.pkcs12
```

Remember to comment out this env varibale (also please note changes to `.env` file): 
```bash
# - KXI_AUTH_DISABLED=1
```


## Q Client

Run `makeCerts.sh` from https://code.kx.com/q/kb/ssl/#certificates and export the following environment variables:
```bash
export SSL_CERT_FILE=$HOME/certs/client-cert.pem 
export SSL_KEY_FILE=$HOME/certs/client-private-key.pem
export SSL_CA_CERT_FILE=$HOME/certs/ca-cert.pem
export SSL_VERIFY_SERVER=NO
```


Start a q process in TLS only mode 
```bash
$ q -E 2 
q).Q.hg`$":https://www.kx.com"              // Test 
"<!DOCTYPE html><html lang=\"en-US\"><head><title>Just a moment...</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset[..]          

q)h:hopen `:tcps://localhost:5051:bob1:password       // wrong user!
'access
  [0]  h:hopen `:tcps://localhost:5051:bob1:password 
         ^
q)h:hopen `:tcps://localhost:5051:bob:password       // connection successful
q)h
9i
```