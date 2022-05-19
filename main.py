import numpy as np
import pandas as pd
import time
import requests
from Strategy import *
from telegram_test import hammer_alert
import sqlalchemy as db
from sqlalchemy import create_engine
  

def main(first_currency, second_currency):
    symbol = first_currency+second_currency
    engine = create_engine('----') # sql engine creator
    seraj_id = 630757965
    amir_id = 98948839

    while True:
        green, red, date, open, close, high, low = \
        hammer(first_currency, second_currency, engine = engine, shadow_body_ratio=2, approximate_ratio=1.0001)
        print('Date: ', date, 'green hammer: ', green, '----', 'red hammer: ', red)

        if green == True or red == True :
            print('high: ',high,' ','low: ',low,' ','close: ',close,' ','open: ',open)
            if green == True :
                hammer_type = 'green'
            elif red == True :
                hammer_type = 'red'
            print('-----------------------------')
            print('==== hammer candle alert ====')
            print('type: ', hammer_type)
            hammer_alert(date, symbol, hammer_type, id = amir_id )
            hammer_alert(date, symbol, hammer_type, id = seraj_id )
            print('-----------------------------')
            time.sleep(100)
        else:
            time.sleep(100)


            
