host_port:"::",last ":" vs first system"docker port kxi-microservices-data-services-sggw-1"
gw:@[hopen;(host_port;5000);0Ni]
if[not null gw;
    show 10 sublist last gw(`.kxi.getData;(`table`startTS`endTS)!(`trade;"p"$.z.d;.z.p);`f;(0#`)!())
    ]
exit 0