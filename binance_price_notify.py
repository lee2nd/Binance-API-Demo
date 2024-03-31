# Line Token applied from https://notify-bot.line.me/zh_TW/
# Binance API Token applied from https://algotrading101.com/learn/binance-python-api-guide/

from binance.client import Client
import requests
import time
import socket

class Binance():
    
    def __init__(self):
        
        self.api_key = 'MYgUFxFMjeVglbzUsips2x38QR11XNJQ5NuYVbov3QBITOcyYmnBGA3MtuHTegWY'
        self.api_secret = 'tOfsgUFcmjb1odifv2F1z4gYjl8Fvbzr5xjbQmiMbNSZnADjRcpCuToHp1H0R2x7'
        self.client = Client(self.api_key,self.api_secret)

    def check_price(self, symbol, interval, drop_percentage):
        
        klines = self.client.futures_klines(symbol=symbol, interval=interval, limit=2)
        # get the current price and previous price  
        curr_close, prev_close = float(klines[-1][4]), float(klines[0][4])
        # calculate the price change percentage
        percentage_change = round(((curr_close-prev_close)/prev_close)*100, 3)
        print(f"{symbol[:-4]} change {percentage_change}% {interval} [{prev_close}⮕{curr_close}]")
        
        if abs(percentage_change) > drop_percentage:  
            if percentage_change < 0:
                return f"{symbol[:-4]} ⬇ {percentage_change*(-1)}% {interval} [{prev_close}⮕{curr_close}]"
            else:
                return f"{symbol[:-4]} ⬆ {percentage_change}% {interval} [{prev_close}⮕{curr_close}]"

def line_notify(message):
    
    headers = {
        "Authorization": "Bearer UAg4tVzgqcgfIvu6cJWvbel2d2VNQPop3v2O0KUGmzI", 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': message}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload, timeout=5)
    
    return r.status_code

sbl_lst = ['BTCUSDT','ETHUSDT']
itvl_lst = [Client.KLINE_INTERVAL_3MINUTE,
            Client.KLINE_INTERVAL_15MINUTE,
            Client.KLINE_INTERVAL_1HOUR,
            Client.KLINE_INTERVAL_4HOUR,
            Client.KLINE_INTERVAL_8HOUR
            ]
drop_pctg_lst = [0.5,    # 3 minutes
                0.75,    # 15 minutes
                1,       # 1 hour
                1.25,    # 4 hours
                1.5      # 8 hours
                ]
retry_counter = 0

# initialize object
b_obj = Binance()

while retry_counter < 5:
    try:    
        
        time.sleep(3)  
        
        for symbol in sbl_lst:
            
            for interval, drop_percentage in zip(itvl_lst,drop_pctg_lst):
                
                # generate the price movement messages
                message = b_obj.check_price(symbol, interval, drop_percentage)
                
                # send line notify message
                line_notify(message)
                
    except socket.error as error:
        
        print("Connection Failed due to socket - {}").format(error)
        print("Attempting {} of 5").format(retry_counter)
        time.sleep(3)
        retry_counter += 1
