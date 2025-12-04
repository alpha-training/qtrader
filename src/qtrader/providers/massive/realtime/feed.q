\l p.q

/ Setup Path
path:"/realtime"
.p.import[`sys;`:path;:;`$path];
.p.e"import stream";

getBatch:{.p.eval"stream.drain_buffer()"};

unixEpoch:1970.01.01D

process:{
    d:flip x`;
    time:unixEpoch+1000000*"j"$d 0;
    sym:`$d 1;
    open:"f"$d 2;
    high:"f"$d 3;
    low:"f"$d 4;
    close:"f"$d 5;
    result:(time;sym;open;high;low;close);
    -1 "Processed ",(string count first result)," rows";
    result
 };

.z.ts:{
    if[count batch:getBatch`;process batch];
 };

\t 1000

/

Few things - Kieran Feedback
- why is there a ` after flip x ? done
- all instances of d[i]; should be d i; done
- you have hard coded a path with your username done
- we should not use show outside of debugging done 
- don't need : on last line done 
- add a newline above .z.ts for readability done
- could you condense .z.ts into one line? e.g. if[count:getBatch`;...]; done
- unixEpoch:1970.01.01D    / will save you typing

