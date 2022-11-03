// internal tables
// with `time` and `sym` columns added by RT client for compatibility
(`$"_prtnEnd")set ([] time:"n"$(); sym:`$(); signal:`$(); endTS:"p"$(); opts:());
(`$"_reload")set ([] time:"n"$(); sym:`$(); mount:`$(); params:(); asm:`$())


// other tables
trade:([] timestamp:"p"$(); sym:`g#`$(); price:"f"$(); size:"j"$())
quote:([] timestamp:"p"$(); sym:`g#`$(); bid:"f"$(); ask:"f"$(); bsize:"j"$(); asize:"j"$())