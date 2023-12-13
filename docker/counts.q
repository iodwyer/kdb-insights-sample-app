gw:hopen "J"$last ":" vs first system"docker port docker-sggw-1"
FileHandle:hopen `:counts.csv



.last.trade:0
.last.quote:0

func1:{
    newCount:count last gw(`.kxi.getData;(`table`startTS`endTS)!(`trade;"p"$.z.d-1;"p"$.z.d+1);`;(0#`)!());
    diff:newCount - .last.trade;
    show raze string[.z.p]," Trade count: ",string[newCount],". Trade Difference: ",string[diff];
    data:csv sv string (.z.p;`trade;newCount;diff);
    FileHandle data,"\n";
    / show raze string[.z.p]," Trade Difference: ",string[diff];
    .last.trade:newCount;
    }

func2:{
    newCount:count last gw(`.kxi.getData;(`table`startTS`endTS)!(`quote;"p"$.z.d-1;"p"$.z.d+1);`;(0#`)!());
    diff:newCount - .last.quote;
    show raze string[.z.p]," Quote count: ",string[newCount],". Quote Difference: ",string[diff];
    data:csv sv string (.z.p;`quote;newCount;diff);
    FileHandle data,"\n";
    / show raze string[.z.p]," Quote Difference: ",string[diff];
    .last.quote:newCount;
    }


func:{func1[];func2[]}
.z.ts:func

\t 5000


writeToCSV:{

    }