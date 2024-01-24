
func1:{[x]
    .dbg.x:x; 
    show "RUNNING MAP FUNC";

    "\n" vs "c"$x
    }

func2:{[x]
    show "LENGTH: ",string count x;
    .dbg.y:x;
    x
    }

func3:{[x]
    show count each x;
    x
    }

parseMsg:{[data]
    f:first each data;
    d:data where f="D";
    p:{(!)."S=|"0: x}each d;
    g:group count each p;

    parseMsgs:{[msgs;grps;typs;cls;lengths]{z$x[y]}[;cls;typs]each (msgs grps[lengths])};

    pM:parseMsgs[p;g;;;];

    tradeMsgs:(28;29;33);
    tradeCols:`5`16`8`9`2500`854`1021`18`5055`55`461`981`111`4;
    tradeTypes:"SPFJJCJPJP*C*J";
    trade:raze pM[tradeTypes;tradeCols;]each tradeMsgs;

    quoteMsgs:(18;19);
    quoteCols:`5`16`12`13`10`9`2000`20`7`55`4;
    quoteTypes:"SPFJFJJPCJJ";
    quote:raze pM[quoteTypes;quoteCols;]each quoteMsgs;

    bTradeMsgs:(10;11);
    bTradeCols:`5`16`55`338`339`4;
    bTradeTypes:"SPPFFJ";
    bTrade:raze pM[bTradeTypes;bTradeCols;]each bTradeMsgs;

    cTradeMsgs:(25;27);
    cTradeCols:`5`16`55`8`252`253`1213`982`1016`113`1229`461`7`5055`255`4;
    cTradeTypes:"SPJFFJ*JJJJ*CJJJ";
    cTrade:raze pM[cTradeTypes;cTradeCols;]each cTradeMsgs;

    mCloseMsgs:(16;21);
    mCloseCols:`5`16`55`301`385`7`5051`5055`4;
    mCloseTypes:"SPP*FCJJJ";
    mClose:raze pM[mCloseTypes;mCloseCols;]each mCloseMsgs;

    dict:`trade`quote`block_trade`cancel_trade`m_close!(trade;quote;bTrade;cTrade;mClose);
    .dbg.dict:dict;
    dict
    }

streamA:.qsp.read.fromAzureStorage["ms://mfs/A_SAMPLE.txt.gz"]
    .qsp.decode.gzip[]
    .qsp.map[func1]
    .qsp.map[func2]
    .qsp.map[parseMsg]
    .qsp.map[func3]
    .qsp.split[]


streamB:streamA 
    .qsp.map[{x`trade}] 
    .qsp.filter[{[x] 1b}; .qsp.use (!) . flip ((`dropEmptyBatches; 1b);(`allowPartials; 1b))] 
    .qsp.write.toVariable[`trade]


streamC:streamA 
    .qsp.map[{x`quote}] 
    .qsp.filter[{[x] 1b}; .qsp.use (!) . flip ((`dropEmptyBatches; 1b);(`allowPartials; 1b))] 
    .qsp.write.toVariable[`quote]

streamD:streamA 
    .qsp.map[{x`cancel_trade;()}] 
    .qsp.filter[{[x] 1b}; .qsp.use (!) . flip ((`dropEmptyBatches; 1b);(`allowPartials; 1b))] 
    .qsp.write.toVariable[`cancel_trade]

.qsp.run (streamB; streamC; streamD)