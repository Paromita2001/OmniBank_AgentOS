from pipeline.timeframe_parser import resolve_timeframe

print(resolve_timeframe("2 days"))
print(resolve_timeframe("yesterday"))
print(resolve_timeframe("last month"))
