// Sample DA custom file.

// Can load other files within this file. Note that the current directory
// is the directory of this file (in this example: /opt/kx/custom).
/ \l subFolder/otherFile1.q
/ \l subFolder/otherFile2.q



.custom.simple:{[table;startTS;endTS;ticker]
    show "Starting .custom.simple from ",string .da.i.dapType;
    
    wc:enlist(in;`sym;enlist ticker);
    res:.kxi.selectTable[table;(startTS;endTS);wc;0b;.kxasm.colNames[table];()];
    res:update dap:.da.i.dapType from res;
    
    show 5 sublist res;
    res
    }


.da.registerAPI[`.custom.simple;
    .sapi.metaDescription[".custom.simple"],
    .sapi.metaParam[`name`type`isReq`description!(`table;-11h;1b;"table")],
    .sapi.metaParam[`name`type`isReq`description!(`startTS;-12h;1b;"start time")],
    .sapi.metaParam[`name`type`isReq`description!(`endTS;-12h;1b;"end time")],
    .sapi.metaParam[`name`type`isReq`description!(`ticker;desc -11 11h;1b;"ticker")],
    .sapi.metaReturn[`type`description!(98h;".custom.simple")],
    .sapi.metaMisc[enlist[`safe]!enlist 1b]
    ]
