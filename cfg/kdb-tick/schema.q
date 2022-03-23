// internal tables 
// with `time` and `sym` columns added by RT client for compatibility
(`$"_prtnEnd")set ([] time:"n"$(); sym:`$(); startTS:"p"$(); endTS:"p"$(); opts:())
(`$"_reload")set ([] time:"n"$(); sym:`$(); mount:`$(); params:())

trade:([] time:"n"$(); sym:`$(); realTime:"p"$(); price:"f"$(); size:"j"$())
quote:([] time:"n"$(); sym:`$(); realTime:"p"$(); bid:"f"$(); ask:"f"$(); bidSize:"j"$(); askSize:"j"$())
xref:flip `time`sym`realTime`serial`nft`factory`batch`machine!"NSPJJJJJ"$\:()
