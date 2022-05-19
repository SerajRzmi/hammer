
# libraries
import pandas as pd
import numpy as np
import requests
import pandas_ta as ta
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import requests

from Database import get_sql


def ma_cross(data, window_1, window_2, window_3):
    moving_averages = ta.Strategy(
    name="moving indicators",
    ta=[
        {"kind": "sma", "length": window_1},
        {"kind": "sma", 'length': window_2},
        {'kind': 'sma', 'length': window_3}
    ])
    data.ta.strategy(moving_averages)
    data.dropna(how= 'any', inplace = True)
    return data




def hammer(first_currency, second_currency, approximate_ratio, shadow_body_ratio, engine):
    ''' 1.approximate ratio range [1:infinite], but too much not recommended, we have no hammer!
        2.shoadow body ratio should be upper than 2'''
    data = get_sql(first_currency, second_currency, engine = engine)
    data = data.astype(float)

    # Green Hammer:
    data['shadow_green'] = data.Open-data.Low
    data['body_green'] = data.Close - data.Open
    data['shadow_body_green'] = data.shadow_green/data.body_green

    # Red Hammer:
    data['shadow_red'] = data.Close - data.Low
    data['body_red'] = data.Open - data.Close
    data['shadow_body_red'] = data.shadow_red/data.body_red
    
    data['green_hammer'] = \
    np.where((data.Open < data.Close) & (data.Close*approximate_ratio >= data.High ) & (data.shadow_body_green > shadow_body_ratio), True, False)
    data['red_hammer'] = \
    np.where((data.Close < data.Open) & (data.Open*approximate_ratio >= data.High ) & (data.shadow_body_red > shadow_body_ratio), True, False)
    data['Positions'] = 0
    data['Positions'] = \
    np.where(data.green_hammer == True, 'green hammer', data.Positions)
    data['Positions'] = \
    np.where(data.red_hammer == True, 'red hammer', data.Positions)


    # output
    position = data.Positions.iloc[-2]
    date = data.index[-2]
    high = data.High.iloc[-2]
    low = data.Low.iloc[-2]
    close = data.Close.iloc[-2]
    open = data.Open.iloc[-2]

    if position == 'green hammer':
        green = True
        red  = False
    elif position == 'red hammer':
        green = False
        red = True
    else:
        green, red = False, False
    
    return green, red, date, open, close, high, low