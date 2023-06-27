    
.z.pg:.z.ps:{show x;value x}

// @param d {dict} Dictionary of user, pass, and HTTP uri, method, headers, body (if relevant)
authorize:{[d]
    show d;
    :$[`bob ~ d`user;
        enlist[`roles]!enlist `$"insights.query.",/:("admin";"sql";"qsql";"custom";"data");
        `code`error!(403;"Everyone except bob is forbidden")];
    }