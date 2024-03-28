// internal tables
// with `time` and `sym` columns added by RT client for compatibility
(`$"_prtnEnd")set ([] time:"n"$(); sym:`$(); signal:`$(); endTS:"p"$(); opts:());
(`$"_reload")set ([] time:"n"$(); sym:`$(); mount:`$(); params:(); asm:`$())
(`$"_heartbeats")set ([] time:"n"$(); sym:`$(); foo:"j"$())
(`$"_batchIngest")set ([] time:"n"$(); sym: `$(); batchUpdType: `$(); session:`$(); address:`$(); callback:(); merge:"b"$(); datacheck:"b"$());
(`$"_batchDelete")set ([] time:"n"$(); sym: `$(); batchUpdType: `$(); session:`$(); address:`$(); callback:(); endTS:"p"$(); filter:(); startTS:"p"$(); table:`$());
(`$"_schemaChange")set ([] time:"n"$(); sym: `$(); batchUpdType: `$(); session:`$(); address:`$(); callback:(); changes:());

// assembly tables
trade:([] time:"p"$(); sym:`g#`$(); price:"f"$(); size:"j"$())
quote:([] time:"p"$(); sym:`g#`$(); bid:"f"$(); ask:"f"$(); bsize:"j"$(); asize:"j"$())
ohlcv:([] time:"p"$(); sym:`g#`$(); open:"f"$(); high:"f"$(); low:"f"$(); close:"f"$(); volume:"j"$())
vwap:([] time:"p"$(); sym:`g#`$(); vwap:"f"$(); accVol:"j"$())