\l p.q
h:hopen 5010;

/ Setup Path
path:"/src/qtrader/providers/massive/realtime"
.p.import[`sys;`:path;:;`$path];
.p.e"import stream";

getBatch:{.p.eval"stream.drain_buffer()"};

unixEpoch:1970.01.01D

process:{
    d:flip x`;
    if[enlist["A"] ~first first x`;tableName:`bar1s];
    if["AM" ~first first x`;tableName:`bar1m];
    time:unixEpoch+1000000*"j"$d 1;
    sym:`$d 2;
    high:"f"$d 3;
    low:"f"$d 4;
    open:"f"$d 5;    
    close:"f"$d 6;
    vol:"j"$d 7;
    result:(time;sym;open;high;low;close;vol);
    neg[h](`.u.upd;tableName;result);
    -1 "Processed ",(string count first result)," rows";
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

