host_port:"::",last ":" vs first system"docker port kxi-microservices-data-services-sggw-1"
gw:@[hopen;(host_port;5000);0Ni]
if[not null gw;
    show 10 sublist last gw(`.kxi.getData;(`table`startTS`endTS)!(`trade;"p"$.z.d;.z.p);`f;(0#`)!())
    ]
// exit 0


// SQL
// 10 sublist last gw(`.kxi.sql;enlist[`query]!enlist"SELECT * FROM trade WHERE (date between '2022.12.19' and '2022.12.20') and (sym = 'AAPL')";`cb;(0#`)!())
/ 
/ getMeta
/ args:`region`startTS`endTS!(`nyc;-0Wp;0Wp)
/ res:last gw(`.kxi.getMeta;args;`;(0#`)!())