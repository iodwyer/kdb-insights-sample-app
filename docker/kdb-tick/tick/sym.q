// internal tables
// with `time` and `sym` columns added by RT client for compatibility
(`$"_prtnEnd")set ([] time:"n"$(); sym:`$(); signal:`$(); endTS:"p"$(); opts:());
(`$"_reload")set ([] time:"n"$(); sym:`$(); mount:`$(); params:(); asm:`$())


// other tables
trade:([] time:"p"$(); sym:`g#`$(); price:"f"$(); size:"j"$())
quote:([] time:"p"$(); sym:`g#`$(); bid:"f"$(); ask:"f"$(); bsize:"j"$(); asize:"j"$())
ohlcv:([] time:"p"$(); sym:`g#`$(); open:"f"$(); high:"f"$(); low:"f"$(); close:"f"$(); volume:"j"$())
vwap: ([] time:"p"$(); sym:`g#`$(); vwap:"f"$(); accVol:"j"$())