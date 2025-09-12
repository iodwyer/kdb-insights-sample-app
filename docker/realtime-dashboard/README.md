## Realtime Dashboard using websockets
The following code subscribes to the websocket publisher and filters by `AAPL` stocks.
```bash
$ cd kdb-insights-sample-app/docker/realtime-dashboard
$ python -m http.server 8888 --bind localhost 
```
![SCR-20250605-qswb.png](./SCR-20250605-qswb.png)

### Testing & Debug
```bash
$ wscat -c ws://localhost:8090/ws/v1/subscribe/websockets-example
Connected (press CTRL+C to quit)
> {"type":"subscribe", "id":33333, "payload":{"topic":"data"}}
< {"payload":{"subscription":"15e0768a-1e21-44fd-8e4e-ebf9113f0efa"},"id":33333,"type":"subscribed"}

< {"payload":{"data":{"size":[64,89,11,76,49],"sym":["MSFT","GOOG","GOOG","INTC","HPQ"],"price":[33.86,77.12,77.08,62.02,39.22],"time":["2025-09-12 01:12:27.737391345","2025-09-12 01:12:27.744566858","2025-09-12 01:12:28.212071629","2025-09-12 01:12:28.477554783","2025-09-12 01:12:28.613580212"]},"subscription":"15e0768a-1e21-44fd-8e4e-ebf9113f0efa"},"id":33333,"type":"update"}

< {"payload":{"data":{"size":[46],"sym":["DELL"],"price":[14.33],"time":["2025-09-12 01:12:28.695642091"]},"subscription":"15e0768a-1e21-44fd-8e4e-ebf9113f0efa"},"id":33333,"type":"update"}
```

