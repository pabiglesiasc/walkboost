import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st

@st.cache_data
def get_data(ss):

    tickers = []

    if ss.stocks=='SP500':
        sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        sp500_tickers = sp500_tickers[0]
        sp500_tickers = sp500_tickers.rename(columns={'Symbol':'Ticker'})
        tickers.append(sp500_tickers.Ticker)
    
    if ss.stocks=='NASDAQ100':
        nasdaq100_tickers = pd.read_html('https://en.wikipedia.org/wiki/NASDAQ-100')
        nasdaq100_tickers = nasdaq100_tickers[4]
        tickers.append(nasdaq100_tickers.Ticker)

    if ss.stocks=='DJIA30':
        djia_tickers = pd.read_html('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')
        djia_tickers = djia_tickers[1]
        djia_tickers = djia_tickers.rename(columns={'Symbol':'Ticker'})
        tickers.append(djia_tickers.Ticker)

    if ss.custom_stocks!='':
        custom_tickers = pd.Series(ss.custom_stocks.split(';'))
        custom_tickers.name = 'Ticker'
        tickers.append(custom_tickers)

    tickers = pd.concat(tickers)
    tickers = tickers.drop_duplicates()
    tickers = tickers.tolist()
    tickers = yf.Tickers(tickers)

    data_ohlcv = tickers.history(start=ss.start_date, end=ss.end_date)
    data_ohlcv.index = pd.to_datetime(data_ohlcv.index, format='%Y-%m-%d', utc=True)
    data_ohlcv = data_ohlcv.resample('D').first()
    data_ohlcv = data_ohlcv.stack()
    data_ohlcv = data_ohlcv.reset_index()
    data_ohlcv = data_ohlcv.rename(columns={'level_1':'Stock'})
    data_ohlcv = data_ohlcv.set_index(['Date', 'Stock']).sort_index()
    data_ohlcv = data_ohlcv.drop(columns=['Dividends', 'Stock Splits'])

    data = data_ohlcv.copy()

    if ss.macroeconomic:

        macroeconomic_tickers = {

            '^GSPC': 'US',
            '^990100-USD-STRD': 'World',
            '^VIX': 'Volatility',
            '^FVX': 'Bonds',
            'GC=F': 'Gold',
            'CL=F': 'Oil',
            'EUR=X': 'EURUSD',
            'GBP=X': 'GBPUSD',
            'CNY=X': 'CNYUSD',
            'JPY=X': 'JPYUSD'

            }

        data_macroeconomic = yf.Tickers(ss.macroeconomic_indicators).history(start='1991-01-01', end='2023-12-31')
        data_macroeconomic.index = pd.to_datetime(data_macroeconomic.index, format='%Y-%m-%d', utc=True)
        data_macroeconomic = data_macroeconomic['Close'].rename(columns=macroeconomic_tickers)
        
        data = pd.merge(left=data.reset_index(), right=data_macroeconomic.reset_index(), on='Date', how='left').set_index(['Date', 'Stock'])

    if ss.correlated:

        data_price = data_ohlcv.Close.unstack()
        corr_stocks = data_price.columns[data_price.notna().sum().gt(252*ss.trading_years)]
        data_corr = data_price.corr().loc[corr_stocks]
        data_corr = data_corr.apply(lambda x: x.nlargest(ss.number_correlated+1).index.tolist()[1:]).T

        def get_price_corr(data_price, x, stock):

            data_price_corr = data_price[x]
            data_price_corr.columns = [f'Corr{i+1}_Close' for i in range(ss.number_correlated)]
            data_price_corr.insert(0, 'Stock', stock)

            return data_price_corr

        data_correlated_stock = data_corr.apply(lambda x: get_price_corr(data_price, x, x.name), axis=1)
        data_correlated_stock = pd.concat(data_correlated_stock.tolist())

        data = pd.merge(left=data.reset_index(), right=data_correlated_stock.reset_index(), on=['Date', 'Stock'], how='left').set_index(['Date', 'Stock'])

        trading_days = data.groupby('Stock').size()
        stocks = trading_days[trading_days.gt(252*ss.trading_years)].index
        data = data.loc[pd.IndexSlice[:, stocks], :]
        data = data.dropna()

    return  data