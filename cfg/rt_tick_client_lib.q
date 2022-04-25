// === internal tables without time/sym columns ===
.rt.NO_TIME_SYM:`$("_prtnEnd";"_reload")

// === rt publish and push functions ===
.rt.push:{'"cannot push unless you have called .rt.pub first"}; // will be overridden


.rt.pub:{[topic]
  if[not 10h=type topic;'"topic must be a string"];
  h:neg hopen hsym`$getenv `KXI_RT_NODES;
  .rt.push:{[nph;payload]
    if[type x:last payload; x:value flip x];
    if[(t:first payload)in .rt.NO_TIME_SYM; x:(count[first x]#'(0Nn;`)),x];
    nph(`.u.upd;t;x);}[h;];
    .rt.push }  

// === rt update and subscribe ===

if[`upd in key `.;  '"do not define upd: rt+tick will implement this"]
if[`end in key `.u; '"do not define .u.end: rt+tick will implement this"]

if[not type key`.rt.upd; .rt.upd:{[payload;idx] '"need to implement .rt.upd"}]

.rt.sub:{[topic;startIdx] 
  if[not 10h=type topic;'"topic must be a string"];

  //connect to the tickerplant
  h:hopen hsym`$getenv `KXI_RT_NODES;

  //initialise our message counter
  .rt.idx:0; 

  // === tick.q will call back to these ===
  upd::{[t;x] if[t in .rt.NO_TIME_SYM; x:2 _x]; .rt.upd[(t;x);.rt.idx]; .rt.idx+:1;};
  .u.end:{.rt.idx:.rt.date2startIdx x+1};

  //replay log file and continue the live subscription
  if[null startIdx;startIdx:0W]; // null means follow only, not start from beginning
  

  {[h;t] h(`.tp.sub;t;`)}[h;] each tables[];
  //subscribe
  // res:h "(.u.sub[`;`]; .u `i`L; .u.d)";

  hclose h;
  
  //if start index is less than current index, then recover
  // if[startIdx<.rt.idx:(.rt.date2startIdx res 2)+res[1;0]; .rt.recoverMultiDay[res[1];startIdx]];
  };


.rt.sub:{[topic;startIdx;uf]
  if[not 10h=type topic;'"topic must be a string"];

  //connect to the tickerplant
  h:hopen hsym`$getenv `KXI_RT_NODES;

  //initialise our message counter
  .rt.idx:0;

  // === tick.q will call back to these ===
  upd::{[uf;t;x]
    if[not type x; x:flip(cols .rt.schema t)!x]; // for log replay 
    if[t in .rt.NO_TIME_SYM; x:`time`sym _x]; 
    uf[(t;x);.rt.idx]; 
    .rt.idx+:1; }[uf];

  .u.end:{.rt.idx:.rt.date2startIdx x+1};

  //replay log file and continue the live subscription
  if[null startIdx;startIdx:0W]; // null means follow only, not start from beginning

  //subscribe
  // res:h "(.u.sub[`;`]; .u `i`L; .u.d)";
  
  {[h;t] h(`.tp.sub;t;`)}[h;] each tables[];
  //.rt.schema:(!/)flip res 0; // used to convert arrays to tables during log replay

  //if start index is less than current index, then recover
  //if[startIdx<.rt.idx:(.rt.date2startIdx res 2)+res[1;0]; 
   //  .rt.recoverMultiDay[res[1];startIdx]]; 
  }

//100 billion records per day
.rt.MAX_LOG_SZ:"j"$1e11

.rt.date2startIdx:{("J"$(string x) except ".")*.rt.MAX_LOG_SZ}

.rt.recoverMultiDay:{[iL;startIdx]
  //iL - index and Log (as can be fed into -11!)
  i:first iL; L:last iL;
  //get all files in the same folder as the tp log file
  files:key dir:first pf:` vs last L;
  //get the name of the logfile itself
  fileName:last pf;
  //get all the lognameXXXX.XX.XX files (logname is sym by default - so usually 
  // the files are of the form sym2021.01.01, sym2021.01.02, sym2021.01.03, etc)
  files:files where files like (-10_ string fileName),"*";
  //from those files, get those with dates in the range we are interested in
  files:` sv/: dir,/:asc files where 
    ("J"$(-10#/:string files) except\: ".")>=startIdx div .rt.MAX_LOG_SZ;
  //set up upd to skip the first part of the file and revert 
  // to regular definition when you hit start index
  upd::{[startIdx;updo;t;x] 
    $[.rt.idx>=startIdx; [upd::updo; upd[t;x]]; .rt.idx+:1]
  }[startIdx;upd];
  //read all of all the log files except the last, where you read up to 'i'
  files:0W,/:files; files[(count files)-1;0]:i;
  //reset .rt.idx for each new day and replay the log file
  {.rt.idx:.rt.date2startIdx "D"$-10#string x 1; -11!x}each files; 
  }


