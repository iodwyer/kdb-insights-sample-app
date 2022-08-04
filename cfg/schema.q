// internal tables 
// with `time` and `sym` columns added by RT client for compatibility
(`$"_prtnEnd") set ([] time:"n"$(); sym:`$(); startTS:"p"$(); endTS:"p"$(); opts:())
(`$"_reload") set ([] time:"n"$(); sym:`$(); mount:`$(); params:())

// other tables
trade:([] sym:`g#`$(); time:"p"$(); price:"f"$(); size:"i"$())