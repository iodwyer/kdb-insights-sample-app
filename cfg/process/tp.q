/load schema

\l cfg/schema.q

.tp.subscriptions:([handle:`int$();table:`symbol$()] syms:());


upd:{[t;d] 
    show "receiving data"; 
    t upsert d;
    }


/sub function
.tp.sub:{[tab;syms]
    /get .z.w
    show "running .tp.sub";
    .tp.subscriptions[(.z.w;tab)]:syms;
    show .tp.subscriptions;
    :.z.D
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

.tp.handleClose:{[h]
    delete from `.tp.subscriptions where handle=h;
    }

init:{[]
    .z.ts:.tp.pubTimer;

    .z.pc:.tp.handleClose;

    system"t 1000";
    }

init[]
