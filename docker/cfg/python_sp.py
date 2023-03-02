from kxi import sp
import datetime

trade_pipeline = (sp.read.from_stream(table='trade',stream="data", prefix="rt-")
    # | sp.decode.json()
    # | sp.map('{[data] (enlist[`timestamp]!enlist `time) xcol enlist "PS*j"$data }')
    # | sp.map(lambda x: ('trade', x))
    | sp.window.tumbling(period = datetime.timedelta(seconds = 10), time_column = 'time', sort=True)
    | sp.map('{[data] 0!select open:first price, high:max price, low:min price, close:last price, volume:sum size by sym, time:(`date$time) + time.minute from data}')
    # | sp.write.to_console())
    | sp.write.to_console())

sp.run(trade_pipeline)