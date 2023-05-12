.qsp.run
 .qsp.read.fromHTTP["https://httpbin.org/anything"; "GET"]   
 .qsp.decode.json[]
/  .qsp.write.toConsole[]
 .qsp.write.toVariable[`output]