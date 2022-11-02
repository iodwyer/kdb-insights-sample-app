.tp.params:.Q.def[`cfg`logDir!`:/opt/kx/cfg`:/opt/kx/tplog] .Q.opt .z.x

// load schema
@[system;"l ",1_string .Q.dd[hsym .tp.params`cfg;`schema.q]]
.tp.logDir:hsym .tp.params`logDir

.tp.subscriptions:([handle:`int$();table:`symbol$()] syms:())

// logging function, responsible for creating and initialising the logfile
// returns handle to logfile
.tp.ld:{[x]

    if[not type key .tp.L:.Q.dd[.tp.logDir;(`$"tp_",string .tp.d)];     // path to logfile;
        .[.tp.L;();:;()]    //  create log file 
    ];

    .tp.i:-11!(-2;.tp.L);    // returns the number of consecutive valid chunks in x and the length of the valid part of the file

    if[0<=type .tp.i;
        -2 (string .tp.L)," is a corrupt log. Truncate to length ",(string last .tp.i)," and restart";
        exit 1
    ];

    :hopen .tp.L

    }
.tp.ts:{[x]

    if[.tp.d<x;
        if[d<x-1;
            system"t 0";
            '"more than one day?"
        ];
    .tp.endofday[]
    ]
    }

// send .u.end msg to subscribers
.tp.end:{[d]
    hndls:(),exec handle from .tp.subscriptions;
    -25!(hndls;(`.u.end;d))
    }

.tp.endofday:{[]
    .tp.end .tp.d;   
    .tp.d+:1;

    if[.tp.l;
        hclose .tp.l;
        .tp.l:.tp.ld[.tp.d]
    ]
    }

.u.upd:{[t;d] 
    .tp.ts[.z.D];   // check time for log rollover
    / -1 "Received data: ",string t;
    if[.tp.l;
      .tp.l enlist (`upd;t;d);
      .tp.i+:1
    ];

    t upsert d;      
    }

// upd for Stream Processor
.u.updSP:{.u.upd[x 0;x 1]}

// sub function
// @ returns schema(s)
.tp.sub:{[t;syms]
    if[`~t;t:.tp.t]; //  all tables
 //   if[not all t in .tp.t;
 //       '"table not found"
  //      ];

    show "running .tp.sub";
    {.tp.subscriptions[(.z.w;x)]:y}[;syms] each t;
    show .tp.subscriptions;
    :.tp.schema[t]  
    }

.tp.pubTimer:{[]
    /check root tables
    .tp.selectAndPub each 0!.tp.subscriptions;

    /wipe tab
    {delete from x} each tables[];
    }

.tp.pub:{[handle;tableName;data]
    show"publishing data";
    handle(`upd;tableName;data)
    }

.tp.selectAndPub:{[sub]
    wc:$[`~sub`syms;();enlist(in;sym;sub`syms)];
    
    toPub:?[sub`table;wc;0b;()];
    
    if[not count toPub;:()];

    .tp.pub[sub`handle;sub`table;toPub];

    }

.tp.handleOpen:{[h]
    -1 "### Process connected on handle: ",string[h],"### Info: ",.Q.s1 (.z.u;.z.a)
    }

.tp.handleClose:{[h]
    delete from `.tp.subscriptions where handle=h;
    }

init:{[]
    .tp.t:tables`.;

    .tp.schema:.tp.t!value each .tp.t;
    
    .tp.d:.z.D;            // today's date
    
    .tp.l:.tp.ld[.tp.d];   // handle to logfile
    
    .z.ts:.tp.pubTimer;
    
    .z.po:.tp.handleOpen;
    .z.pc:.tp.handleClose;

    system"t 1000";
    }

init[]

