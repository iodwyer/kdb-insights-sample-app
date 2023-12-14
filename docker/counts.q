gw:hopen "J"$last ":" vs first system"docker port docker-sggw-1"
FileHandle:hopen `:counts.csv
tabs:`trade`quote

`.last set tabs!count[tabs]#0

writeToCSV:{[time;n;d;t]
    show raze string[time]," ",string[t]," count: ",string[n],". ",string[t]," difference: ",string[d];
    data:csv sv string (time;t;n;d);
    FileHandle data,"\n";
    }

queryAndWrite:{[p;t]
    newCount:count last gw(`.kxi.getData;(`table`startTS`endTS)!(t;"p"$.z.d;"p"$.z.d+1);`;(0#`)!());
    diff:newCount - .last[t];
    writeToCSV[p;newCount;diff;t];
    .last[t]:newCount;
    }

readCSV:{[f]
    flip`time`table`tab_count`diff!("PSJJ";csv) 0: f
    }

.pivot.simple:{[tab; keycol; pivcol; valcol]
    P:asc distinct ?[tab; (); (); pivcol];
    / pivcol:`$(string[tabs]),\: "_",string valcol;
    :?[tab; (); enlist[keycol]!enlist keycol; (#; `P; (!; pivcol; valcol))]
    };

.z.ts:{queryAndWrite[.z.p;] each tabs}

\t 5000