# to see if picks eventually hit based on choices you or others took in the past
import os
import yfinance as yf
import pandas as pd
import get_stk_data

pd.options.mode.chained_assignment = None  # default='warn'


# pull date, current price, dates high, and dates low info from data
# data result example calling for AAPL:
# |Date|Adj Close|Close|High||Low|Open|Volume|Symbol
# |1/15/20|76.69576263|77.83499908|78.875|77.38749695|77.96250153|121923600|AAPL
# |1/16/20|77.65648651|78.80999756|78.92500305|78.02249908|78.39749908|108829200|AAPL
def open_csv():
    if not os.path.exists('trades.csv'):
        print ('''
            Missing file:trades.csv. Create it and save to same directory as the script your running for it.
            Columns to use, and in this order, are :
            Entry Date	
            Stock Symbol	
            Long/Short	
            Entry Price	
            Stop Loss
            ''')
        return 0

    data = pd.read_csv('trades.csv')
    return data

# determine if a long trade or short, then call the right function
def sort_and_process(directoryz):
    tradez = pd.read_csv('trades.csv')
    long_hits = 0
    short_hits = 0
    longs = 0
    shorts = 0
    for ind in tradez.index:
        if tradez['Long/Short'][ind] == 'Long':
            longs = longs + 1
            long_hits = long_hits + long_target_hit(tradez.loc[[ind]], directoryz)
        elif tradez['Long/Short'][ind] == 'Short':
            shorts = shorts + 1
            short_hits = short_hits + short_target_hit(tradez.loc[[ind]], directoryz)

    long_testing = float((long_hits * 100) / longs)
    short_testing = float((short_hits * 100) / shorts)
    print '''
    ******************************************************************
    * Out of {} LONG trades, {} hit PT eventually                  
    * Winning average for them is {}%                               
    ******************************************************************
    '''.format(longs, long_hits, long_testing)

    print '''
    ******************************************************************
    * Out of {} SHORT trades, {} hit PT eventually                 
    * Winning average for them is {}%                               
    ******************************************************************
    '''.format(shorts, short_hits, short_testing)

    return 0


# long - determine if it ever hit the PT ((entry - stop) * 2) + entry
def long_target_hit(tickers, directoryz):
    hits = 0
    for ind in tickers.index:
        data = pd.read_csv('{}/{}.csv'.format(directoryz, tickers['Stock Symbol'][ind]))
        tickers['Entry Price'] = tickers['Entry Price'].replace('\$', '', regex=True).astype(float)
        tickers['Entry Price'] = tickers['Entry Price'].replace('\,', '', regex=True).astype(float)
        tickers['Stop Loss'] = tickers['Stop Loss'].replace('\$', '', regex=True).astype(float)
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        tickers['Entry Date'] = pd.to_datetime(tickers['Entry Date'], errors='coerce')

        target = tickers['Entry Price'][ind] + ((pd.to_numeric(tickers['Entry Price'][ind])
                                                 - pd.to_numeric(tickers['Stop Loss'][ind])) * 2)
        for indy in data.index:
            if data['High'][indy] >= target and data['Date'][indy] >= tickers['Entry Date'][ind]:
                print ('LONG Ticker = {} -> Entry = {} -> PT = {} -> PT hit {} -> Days High {}'
                       .format(data['Symbol'][indy], tickers['Entry Date'][ind], target, data['Date'][indy],
                               data['High'][indy]))
                hits = hits + 1
                break
            continue
    return hits


# short - determine if it ever hit the PT ((stop -  entry) * 2) - entry
def short_target_hit(tickers, directoryz):
    hits = 0
    for ind in tickers.index:
        data = pd.read_csv('{}/{}.csv'.format(directoryz, tickers['Stock Symbol'][ind]))
        tickers['Entry Price'] = tickers['Entry Price'].replace('\$', '', regex=True).astype(float)
        tickers['Entry Price'] = tickers['Entry Price'].replace('\,', '', regex=True).astype(float)
        tickers['Stop Loss'] = tickers['Stop Loss'].replace('\$', '', regex=True).astype(float)
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        tickers['Entry Date'] = pd.to_datetime(tickers['Entry Date'], errors='coerce')
        target = tickers['Entry Price'][ind] - ((pd.to_numeric(tickers['Stop Loss'][ind])
                                                 - pd.to_numeric(tickers['Entry Price'][ind])) * 2)

        for indy in data.index:
            if data['High'][indy] <= target and data['Date'][indy] >= tickers['Entry Date'][ind]:
                print ('SHORT Ticker = {} -> Entry = {} -> PT = {} -> PT hit {} -> Days Low {}'
                       .format(data['Symbol'][indy], tickers['Entry Date'][ind], target, data['Date'][indy],
                               data['Low'][indy]))
                hits = hits + 1
                break
            continue
    return hits


directory = 'tickers_directory'
trades = open_csv()

# get ticker info from yfinance
get_stk_data.get_ticker_data(trades, directory)

# determine if long or short, send to right process call
sort_and_process(directory)

exit()
