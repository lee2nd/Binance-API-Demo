import pandas as pd
from datetime import datetime
from binance.client import Client
from binance.enums import HistoricalKlinesType

# the binance api link
# https://python-binance.readthedocs.io/en/latest/binance.html

# you can get the api key and api secret from the binance website
api_key = "MYgUFxFMjeVglbzUsips2x38QR11XNJQ5NuYVbov3QBITOcyYmnBGA3MtuHTegWY"
api_secret = "tOfsgUFcmjb1odifv2F1z4gYjl8Fvbzr5xjbQmiMbNSZnADjRcpCuToHp1H0R2x7"
client = Client(api_key, api_secret)

# get the ETH to usdt real time price
klines = client.get_historical_klines(
                symbol ='ETHUSDT',                             # ETH
                interval = Client.KLINE_INTERVAL_1MINUTE,      # fetch 1 minute klines until now
                limit = 1,                                     # only get the last data
                klines_type  = HistoricalKlinesType.FUTURES    # choose the FUTURES 
                )

# you can hide following 3 lines, it shows the detailed information
df = pd.DataFrame(klines)
df.columns = ['Open_time','open','high','low','close','volume','Close_time', 'Quote asset volume', 'number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']   
print(df)

# the close time
print(datetime.fromtimestamp(int(str(klines[0][6])[:10])))

# the real-time close price
print(klines[0][4])  

# sample output
# 2022-10-29 23:26:59
# 1625.87