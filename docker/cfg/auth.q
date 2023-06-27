/ .z.pw:{[user;pswd]
/     show(user;pswd);
/     res:authorize `user`pswd!(user;pswd);
/     :$[`roles in key res;
/         1b;
/         0b
/     ]
/     }

.z.po:{show "Port open";}

.z.pg:.z.ps:{show x;value x}

// @param d {dict} Dictionary of user, pass, and HTTP uri, method, headers, body (if relevant)
authorize:{[d]
    show d;
    :$[`bob ~ d`user;
        enlist[`roles]!enlist `$"insights.query.",/:("admin";"sql";"qsql";"custom";"data");
        `code`error!(403i;"Everyone except bob is forbidden")];
    }