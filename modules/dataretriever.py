import pandas as pd
import numpy as np

def get_yfinance():
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'yfinance'])
    import yfinance as yf





def get_data(start_date, end_date, stocks, macroeconomic, correlated, extra_stocks, macroeconomic_indicators, number_correlated):
    return None