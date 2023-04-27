dst:`:data/hdb/data      / database root
dst:`:data/hdb/staging/backfill
dates:.z.d-til 10
n:100

genDataTrade:{[x] ([]time:"p"$x; sym:n?`IBM`GOOG`AMD; price:n?100f; size:n?50)}
genDataQuote:{[x] ([]time:"p"$x; sym:n?`IBM`GOOG`AMD; bid:n?100f; ask:n?100f; bsize:n?50; asize:n?50)}

write:{[tab;dt;data]
    t:.Q.en[dst] update sym:`p#sym from `sym xasc data;
    .Q.dd[dst;(dt;tab;`)] set t;
    }

{[dt]
    write[`trade;dt;] genDataTrade[dt];
    write[`quote;dt;] genDataQuote[dt];
    } each dates

"Run: chmod -R 777 data"
exit 0