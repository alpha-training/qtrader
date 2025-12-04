\l p.q

/ Setup Path
path:"/home/ehutton/qtrader/src/qtrader/providers/massive/realtime"
.p.import[`sys;`:path;:;`$path];
.p.e"import stream";

getBatch:{.p.eval"stream.drain_buffer()"};

unixEpoch:1970.01.01D00:00:00.000000000;

process:{
    d:flip x`;
    time:unixEpoch+1000000*"j"$d[0];
    sym:`$d[1];
    open:"f"$d[2];
    high:"f"$d[3];
    low:"f"$d[4];
    close:"f"$d[5];
    result:(time;sym;open;high;low;close);
    -1 "Processed ",(string count first result)," rows";
    show result;
    :result
 };
.z.ts:{
    batch:getBatch[];
    if[count batch;process batch];
 };

\t 1000

/

Few things - Kieran Feedback
- why is there a ` after flip x ?
- all instances of d[i]; should be d i;
- the result, can you not do that on one line?
- you have hard coded a path with your username
- we should not use show outside of debugging
- don't need : on last line
- add a newline above .z.ts for readability
- could you condense .z.ts into one line? e.g. if[count:getBatch`;...];
- unixEpoch:1970.01.01D    / will save you typing

