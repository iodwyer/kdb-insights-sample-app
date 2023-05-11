.qsp.run
  .qsp.read.fromKafka["subway"; "34.130.174.118:9091"]
  .qsp.decode.json[]
  .qsp.write.toConsole[]