//
// @desc Define a new API. Counts number of entries by specified columns.
//
// @param table		{symbol}			Table name.
// @param byCols	{symbol|symbol[]}	Column(s) to count by.
// @param startTS	{timestamp}			Start time (inclusive).
// @param endTS		{timestamp}			End time (exclusive).
//
// @return			{table}				Count by specified columns.
//
.custom.countBy:{[table;startTS;endTS;byCols]
	bc:$[not[`date in cols table]&`date in byCols;
		(x,`date)!(x:(byCols,())except`date),enlist($;"d";`time);
		x!x:byCols,()];

	?[table;enlist(within;`timestamp;(startTS;endTS-1));bc;enlist[`cnt]!enlist(count;`i)]
	}

.da.registerAPI[`.custom.countBy;
	.sapi.metaDescription["Test custom API - does a count by."],
	.sapi.metaMisc[enlist[`safe]!enlist 1b],
	.sapi.metaParam[`name`type`isReq`description!(`table;-11h;1b;"Table name.")],
	.sapi.metaParam[`name`type`isReq`description!(`byCols;-11 11h;1b;"Column(s) to count by.")],
	.sapi.metaParam[`name`type`isReq`description!(`startTS;-12h;1b;"Start time (inclusive).")],
	.sapi.metaParam[`name`type`isReq`description!(`endTS;-12h;1b;"End time (exclusive).")],
	.sapi.metaReturn`type`description!(98h;"Count by specified columns.")]

