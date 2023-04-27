/ curl -X POST $SM/ingest -H 'Content-Type: application/json' -d '{"name":"backfill"}' 

runIngest:{[]
    headers:enlist["Content-Type"]!enlist "application/json";
    body:.j.j enlist[`name]!enlist `backfill;
    queryEndpoint:"http://",(trim last "->" vs first system"docker port docker-sm-1"),"/ingest";
    -1 queryEndpoint;
    resp:.kurl.sync (queryEndpoint; `POST;`headers`body!(headers;body));
    resp
    }

runIngest[]