// internal tables
// with `time` and `sym` columns added by RT client for compatibility
(`$"_prtnEnd")set ([] time:"n"$(); sym:`$(); signal:`$(); endTS:"p"$(); opts:());
(`$"_reload")set ([] time:"n"$(); sym:`$(); mount:`$(); params:(); asm:`$())


// other tables
trade:([] time:"p"$(); sym:`g#`$(); price:"f"$(); size:"j"$())
quote:([] time:"p"$(); sym:`g#`$(); bid:"f"$(); ask:"f"$(); bsize:"j"$(); asize:"j"$())
ohlcv:([] sym:`g#`$(); time:"p"$(); open:"f"$(); high:"f"$(); low:"f"$(); close:"f"$(); volume:"j"$())
vwap:([] sym:`g#`$(); time:"p"$(); vwap:"f"$(); accVol:"j"$())