# to see if picks eventually hit based on choices you or others took in the past
import datetime
import os
import yfinance as yf
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


# pull date, current price, dates high, and dates low info from data
# data result example calling for AAPL:
# |Date|Adj Close|Close|High||Low|Open|Volume|Symbol
# |1/15/20|76.69576263|77.83499908|78.875|77.38749695|77.96250153|121923600|AAPL
# |1/16/20|77.65648651|78.80999756|78.92500305|78.02249908|78.39749908|108829200|AAPL
def get_ticker_data(tickers, directoryz):
    for ind in tickers.index:
        if not os.path.exists(directoryz):
            os.makedirs(directoryz)
        if not os.path.exists('{}/{}.csv'.format(directoryz, tickers['Symbol'][ind])):
            try:

                # print('Getting data for: {}'.format(tickers['Symbol'][ind]))
                # print price_target
                df = yf.download(tickers['Symbol'][ind], period='2y', interval='1d')
                df.dropna(inplace=True)
                df["Symbol"] = tickers['Symbol'][ind]
                df.to_csv('{}/{}.csv'.format(directoryz, tickers['Symbol'][ind]))

            except Exception as ex:
                print('Error:', ex)
        else:
            print('-> Already have {}.csv file so skipping'.format(tickers['Symbol'][ind]))


# determine if short or long
def long_or_short():
    pass


# long - determine if it ever hit the PT ((entry - stop) * 2) + entry
def long_target_hit(tickers, directoryz):
    print ("Scanning for Long Price Target hits")
    hits = 0
    ticker_hits = []
    ticker_misses = []
    for ind in tickers.index:
        # print ('Opening {}.csv'.format(tickers['Symbol'][ind]))
        # print('Parsing data to see if {} ever hit ${}'.format(tickers['Symbol'][ind],tickers['Target'][ind]))
        data = pd.read_csv('{}/{}.csv'.format(directoryz, tickers['Symbol'][ind]))
        tickers['Date'][ind] = pd.to_datetime(tickers['Date'][ind], errors='coerce')

        for indy in data.index:
            data['Date'][indy] = pd.to_datetime(data['Date'][indy], errors='coerce')

            if data['High'][indy] >= tickers['Target'][ind] and data['Date'][indy] >= tickers['Date'][ind]:
                print ('Ticker = {} -> Entry Date = {} -> PT = {} -> PT hit on {} and had a high of {}'
                       .format(data['Symbol'][indy], tickers['Date'][ind], tickers['Target'][ind], data['Date'][indy],
                               data['High'][indy]))
                hits = hits + 1
                ticker_hits.append(data['Symbol'][indy])
                break
            continue

        ticker_misses = [item for item in tickers['Symbol'] if item not in ticker_hits]
    print ('\n\nHits total = {} \nOut of a total of {} ideas.'.format(hits, len(tickers)))
    print ('Tickers that hit: {}'.format(ticker_hits))
    print ('Tickers that missed: {}'.format(ticker_misses))

    return 0


# short - determine if it ever hit the PT ((stop -  entry) * 2) - entry
def short_target_hit(short_tickers, directory_s):
    print ("Scanning for Short Price Target hits")
    hits = 0
    ticker_hits = []
    ticker_misses = []
    for ind in short_tickers.index:
        # print ('Opening {}.csv'.format(tickers['Symbol'][ind]))
        # print('Parsing data to see if {} ever hit ${}'.format(tickers['Symbol'][ind],tickers['Target'][ind]))
        data = pd.read_csv('{}/{}.csv'.format(directory_s, short_tickers['Symbol'][ind]))
        short_tickers['Date'][ind] = pd.to_datetime(short_tickers['Date'][ind], errors='coerce')

        for indy in data.index:
            data['Date'][indy] = pd.to_datetime(data['Date'][indy], errors='coerce')

            if data['Low'][indy] <= short_tickers['Target'][ind] and data['Date'][indy] >= short_tickers['Date'][ind]:
                print ('Ticker = {} -> Entry Date = {} -> PT = {} -> PT hit on {} and had a high of {}'
                       .format(data['Symbol'][indy], short_tickers['Date'][ind], short_tickers['Target'][ind],
                               data['Date'][indy],
                               data['High'][indy]))
                hits = hits + 1
                ticker_hits.append(data['Symbol'][indy])
                break
            continue

        ticker_misses = [item for item in short_tickers['Symbol'] if item not in ticker_hits]
    print ('\n\nHits total = {} \nOut of a total of {} ideas.'.format(hits, len(short_tickers)))
    print ('Tickers that hit: {}'.format(ticker_hits))
    print ('Tickers that missed: {}'.format(ticker_misses))

    return 0


# TESTING VARs AND WHAT NOT
# ticker_info = {'Symbol': ['AAL', 'VISL', 'SHWZ', 'AMD'],
#       'Target': [20, 1000, 1000, 91.97],
#        'Date': [datetime.datetime(2021,01,15), datetime.datetime(2021,01,15),
#                 datetime.datetime(2021,01,19), datetime.datetime(2021,02,04)]}

directory = 'targetHitEventually'

# LONGS
long_ticker_info = {
    'Symbol': ['AUPH', 'MBIO', 'AEP', 'SHWZ', 'ELYS', 'VLNCF', 'ZAGG', 'YELL', 'AQUA', 'SOS', 'T', 'IBM',
               'MILE', 'LFMD', 'SNAP', 'PYPL', 'K', 'TLRY', 'TLT', 'TLT', 'GDDY', 'JUVAF', 'T', 'NPA',
               'TSIA', 'NIO', 'CLVS', 'U', 'FEYE', 'MDT', 'DASH', 'SH', 'ASTS', 'CVM', 'JOB', 'NET',
               'FEYE', 'DFLYF', 'SBRA', 'VIAC', 'KALV', 'PRQR', 'ACAD', 'GEO', 'REI', 'DASH', 'SIEN',
               'GPRO', 'GBTC', 'ARVL', 'BLUE', 'GSAT', 'DNN', 'TLLTF', 'GPRO', 'WISH', 'BBIG', 'ETHE',
               'CIEN', 'BKI', 'AYX', 'LULU', 'SOFI', 'GNLN', 'GPRO', 'YALA', 'HUT', 'GNLN', 'POLA',
               'SNPR', 'SFTW', 'DFLYF', 'BABA', 'WISH', 'PENN', 'SUMO', 'FXI', 'BBIG', 'GNLN', 'ETHE',
               'DFLYF', 'CVS', 'HUT', 'KYMR', 'CIDM', 'ADMP', 'VXRT', 'SOFI', 'DPRO', 'AUPH', 'PLTR',
               'ARRY', 'GNLN', 'DPRO', 'IGT', 'BTBT', 'VXRT', 'COIN', 'AYX', 'AUPH', 'ARRY', 'LTCH',
               'SRPT', 'OGI', 'ABNB', 'BTBT', 'SQQQ', 'SLV', 'T', 'REFR', 'CTRM', 'SLV', 'LQMT', 'ATIF',
               'RIDE', 'NURO', 'LOW', 'MDIA', 'RWLK', 'REI', 'BLUE', 'IPOF', 'BBKCF', 'OSCR', 'MAPS',
               'FIZZ', 'SOFI', 'VERB', 'HOOD', 'QS', 'CBAY', 'PENN', 'TRIP', 'DPRO', 'GME', 'JKS', 'BTBT',
               'MNKD', 'UAL', 'IRNT', 'FUBO', 'PSLV', 'BBBY', 'BKKT', 'GLD', 'BKD', 'ZKIN', 'BITF', 'XSPA'],
    'Target': [14.02, 5.22, 84.38, 2.36, 8.41, 2.23, 4.68, 7.82, 27.25, 8.31, 32.18, 135.56,
               11.96, 22.22, 60.79, 259.22, 63.90, 39.78, 139.04, 144.44, 81.21, 1.06, 32.54,
               15.44, 11.99, 40.84, 8.40, 117.32, 20.22, 126.26, 147.16, 17.15, 9.70, 19.42,
               0.70, 80.96, 20.92, 1.81, 18.22, 46.80, 30.40, 7.60, 24.52, 6.80, 2.94, 162.22,
               8.46, 10.86, 39.79, 23.52, 36.60, 1.94, 1.62, 0.70, 13.68, 15.13, 6.39, 18.92,
               59.24, 76.26, 95.72, 366.82, 19.02, 5.00, 12.93, 22.00, 6.64, 5.21, 12.62, 10.32,
               10.24, 1.55, 203.45, 13.12, 75.80, 24.06, 46.41, 4.66, 4.62, 17.54, 1.76, 86.45,
               5.84, 69.24, 2.08, 1.27, 9.58, 19.55, 4.67, 16.92, 28.14, 22.56, 3.00, 3.39,
               19.14, 16.64, 9.66, 294.34, 85.34, 15.88, 22.18, 12.22, 87.62, 3.23, 166.44,
               16.98, 8.04, 24.14, 28.93, 2.99, 3.04, 23.63, 0.14, 5.32, 8.20, 16.23, 211.20,
               11.32, 3.37, 3.58, 21.62, 10.78, 1.44, 20.80, 17.34, 56.90, 18.78, 2.74,
               47.74, 26.10, 4.70, 88.32, 41.32, 5.26, 230.20, 62.72, 15.50, 5.19, 51.84,
               16.88, 37.00, 9.25, 24.58, 28.60, 186.38, 7.15, 3.40, 9.60, 1.98],
    'Date': [datetime.datetime(2021, 1, 8), datetime.datetime(2021, 1, 11), datetime.datetime(2021, 1, 15),
             datetime.datetime(2021, 1, 19), datetime.datetime(2021, 1, 27), datetime.datetime(2021, 1, 28),
             datetime.datetime(2021, 2, 8), datetime.datetime(2021, 2, 16), datetime.datetime(2021, 2, 25),
             datetime.datetime(2021, 2, 25), datetime.datetime(2021, 3, 8), datetime.datetime(2021, 3, 8),
             datetime.datetime(2021, 3, 8), datetime.datetime(2021, 3, 9), datetime.datetime(2021, 3, 10),
             datetime.datetime(2021, 3, 10), datetime.datetime(2021, 3, 16), datetime.datetime(2021, 3, 16),
             datetime.datetime(2021, 3, 17), datetime.datetime(2021, 3, 19), datetime.datetime(2021, 3, 26),
             datetime.datetime(2021, 3, 26), datetime.datetime(2021, 3, 29), datetime.datetime(2021, 3, 29),
             datetime.datetime(2021, 3, 29), datetime.datetime(2021, 3, 30), datetime.datetime(2021, 3, 31),
             datetime.datetime(2021, 3, 30), datetime.datetime(2021, 4, 5), datetime.datetime(2021, 4, 12),
             datetime.datetime(2021, 4, 12), datetime.datetime(2021, 4, 15), datetime.datetime(2021, 4, 20),
             datetime.datetime(2021, 4, 20), datetime.datetime(2021, 4, 21), datetime.datetime(2021, 4, 22),
             datetime.datetime(2021, 4, 23), datetime.datetime(2021, 4, 26), datetime.datetime(2021, 5, 7),
             datetime.datetime(2021, 5, 12), datetime.datetime(2021, 5, 17), datetime.datetime(2021, 5, 17),
             datetime.datetime(2021, 5, 17), datetime.datetime(2021, 5, 17), datetime.datetime(2021, 5, 18),
             datetime.datetime(2021, 5, 24), datetime.datetime(2021, 5, 24), datetime.datetime(2021, 5, 24),
             datetime.datetime(2021, 5, 26), datetime.datetime(2021, 5, 26), datetime.datetime(2021, 5, 28),
             datetime.datetime(2021, 6, 1), datetime.datetime(2021, 6, 1), datetime.datetime(2021, 6, 9),
             datetime.datetime(2021, 6, 11), datetime.datetime(2021, 6, 15), datetime.datetime(2021, 6, 22),
             datetime.datetime(2021, 6, 22), datetime.datetime(2021, 6, 22), datetime.datetime(2021, 6, 21),
             datetime.datetime(2021, 6, 22), datetime.datetime(2021, 6, 21), datetime.datetime(2021, 6, 28),
             datetime.datetime(2021, 6, 29), datetime.datetime(2021, 6, 30), datetime.datetime(2021, 7, 1),
             datetime.datetime(2021, 7, 2), datetime.datetime(2021, 7, 1), datetime.datetime(2021, 7, 6),
             datetime.datetime(2021, 7, 6), datetime.datetime(2021, 7, 6), datetime.datetime(2021, 7, 7),
             datetime.datetime(2021, 7, 8), datetime.datetime(2021, 7, 9), datetime.datetime(2021, 7, 12),
             datetime.datetime(2021, 7, 12), datetime.datetime(2021, 7, 12), datetime.datetime(2021, 7, 12),
             datetime.datetime(2021, 7, 13), datetime.datetime(2021, 7, 20), datetime.datetime(2021, 7, 23),
             datetime.datetime(2021, 7, 23), datetime.datetime(2021, 8, 2), datetime.datetime(2021, 8, 2),
             datetime.datetime(2021, 8, 2), datetime.datetime(2021, 8, 6), datetime.datetime(2021, 8, 6),
             datetime.datetime(2021, 8, 6), datetime.datetime(2021, 8, 4), datetime.datetime(2021, 8, 9),
             datetime.datetime(2021, 8, 18), datetime.datetime(2021, 8, 17), datetime.datetime(2021, 8, 17),
             datetime.datetime(2021, 8, 18), datetime.datetime(2021, 8, 23), datetime.datetime(2021, 8, 23),
             datetime.datetime(2021, 8, 23), datetime.datetime(2021, 8, 23), datetime.datetime(2021, 8, 23),
             datetime.datetime(2021, 8, 23), datetime.datetime(2021, 8, 23), datetime.datetime(2021, 8, 23),
             datetime.datetime(2021, 8, 25), datetime.datetime(2021, 8, 31), datetime.datetime(2021, 8, 30),
             datetime.datetime(2021, 8, 30), datetime.datetime(2021, 9, 1), datetime.datetime(2021, 9, 2),
             datetime.datetime(2021, 9, 2), datetime.datetime(2021, 9, 13), datetime.datetime(2021, 9, 15),
             datetime.datetime(2021, 9, 15), datetime.datetime(2021, 9, 20), datetime.datetime(2021, 9, 20),
             datetime.datetime(2021, 9, 19), datetime.datetime(2021, 9, 22), datetime.datetime(2021, 9, 21),
             datetime.datetime(2021, 9, 21), datetime.datetime(2021, 9, 22), datetime.datetime(2021, 9, 27),
             datetime.datetime(2021, 9, 27), datetime.datetime(2021, 9, 28), datetime.datetime(2021, 9, 30),
             datetime.datetime(2021, 9, 30), datetime.datetime(2021, 10, 4), datetime.datetime(2021, 10, 5),
             datetime.datetime(2021, 10, 7), datetime.datetime(2021, 10, 7), datetime.datetime(2021, 10, 11),
             datetime.datetime(2021, 10, 11), datetime.datetime(2021, 10, 12),
             datetime.datetime(2021, 10, 15),
             datetime.datetime(2021, 10, 15), datetime.datetime(2021, 10, 20),
             datetime.datetime(2021, 10, 19),
             datetime.datetime(2021, 10, 19), datetime.datetime(2021, 10, 20),
             datetime.datetime(2021, 10, 22),
             datetime.datetime(2021, 10, 26), datetime.datetime(2021, 10, 29),
             datetime.datetime(2021, 11, 1),
             datetime.datetime(2021, 11, 8), datetime.datetime(2021, 11, 11),
             datetime.datetime(2021, 11, 12),
             datetime.datetime(2021, 11, 17), datetime.datetime(2021, 11, 18),
             datetime.datetime(2021, 11, 17),
             datetime.datetime(2021, 1, 23), datetime.datetime(2021, 1, 24)]}

# SHORTS
short_ticker_info = {'Symbol': ['NVDA', 'TWTR', 'AAPL', 'PTON', 'PTON', 'SPY', 'IWM', 'PLUG',
                                'SNAP', 'UAA', 'SPY', 'LULU', 'IWM',
                                'MAT', 'GBTC', 'LEN', 'SNBR', 'IWM', 'KSS', 'MAT', 'XLF', 'KSS', 'FITB', 'LIN', 'IYT',
                                'LOW', 'LB',
                                'CAKE', 'FB', 'BBD', 'SPY', 'KSS', 'CAKE', 'FITB', 'XLF', 'WSC', 'FB', 'LIN', 'IWM',
                                'PXD', 'STNE',
                                'IP', 'XLF', 'ATH', 'XLF', 'ORI', 'DELL', 'SLM', 'LOW', 'CCI', 'AMAT', 'CNQ', 'ATH',
                                'AFL', 'TMUS',
                                'AMAT', 'TMUS', 'TGT', 'NKE', 'YUM', 'YUM', 'DELL', 'REGN', 'TEAM', 'PANW', 'ZTS',
                                'INVH', 'ARKK',
                                'EGP', 'WD', 'SPG', 'XHB', 'XRT', 'AAPL', 'ZS', 'CTAS', 'BR', 'DIS', 'KSS', 'SPG', 'WK',
                                'PZZA',
                                'DIS', 'TSLA', 'CARR', 'MS', 'U', 'EPI'],
                     'Target': [439.36, 44.66, 110.90, 128.78, 132.84, 340.25, 209.68, 43.58, 60.07,
                                21.50, 389.68, 272.22, 200.94, 20.26, 36.78, 99.92, 98.04, 200.42,
                                50.28, 18.26, 35.48, 48.60, 37.12, 280.82, 251.26, 179.44, 58.40,
                                48.20, 313.78, 4.96, 423.08, 50.84, 46.33, 36.00, 35.20, 25.10,
                                335.22, 275.40, 218.03, 138.82, 57.02, 59.57, 34.62, 59.82, 34.08,
                                23.04, 91.16, 16.48, 177.98, 185.50, 131.48, 28.10, 56.52, 54.47,
                                136.22, 112.71, 134.52, 229.39, 159.74, 127.64, 126.08, 90.54,
                                614.38, 356.95, 433.17, 196.13, 37.52, 107.76, 161.25, 100.29, 121.80,
                                68.64, 87.60, 134.26, 232.00, 319.90, 152.88, 161.24, 40.54, 121.23,
                                121.62, 110.28, 159.05, 1055.00, 45.92, 90.74, 158.94, 32.50],
                     'Date': [datetime.datetime(2021, 1, 6), datetime.datetime(2021, 1, 8),
                              datetime.datetime(2021, 1, 11), datetime.datetime(2021, 1, 11),
                              datetime.datetime(2021, 1, 19), datetime.datetime(2021, 2, 8),
                              datetime.datetime(2021, 2, 10), datetime.datetime(2021, 2, 16),
                              datetime.datetime(2021, 2, 24), datetime.datetime(2021, 3, 22),
                              datetime.datetime(2021, 4, 5), datetime.datetime(2021, 4, 5),
                              datetime.datetime(2021, 4, 13), datetime.datetime(2021, 5, 3),
                              datetime.datetime(2021, 5, 4), datetime.datetime(2021, 5, 4),
                              datetime.datetime(2021, 5, 4), datetime.datetime(2021, 5, 6),
                              datetime.datetime(2021, 6, 2), datetime.datetime(2021, 6, 14),
                              datetime.datetime(2021, 6, 14), datetime.datetime(2021, 6, 14),
                              datetime.datetime(2021, 6, 14), datetime.datetime(2021, 6, 14),
                              datetime.datetime(2021, 6, 14), datetime.datetime(2021, 6, 14),
                              datetime.datetime(2021, 6, 15), datetime.datetime(2021, 6, 17),
                              datetime.datetime(2021, 6, 21), datetime.datetime(2021, 6, 25),
                              datetime.datetime(2021, 7, 1), datetime.datetime(2021, 7, 6),
                              datetime.datetime(2021, 7, 6), datetime.datetime(2021, 7, 6),
                              datetime.datetime(2021, 7, 6), datetime.datetime(2021, 7, 6),
                              datetime.datetime(2021, 7, 7), datetime.datetime(2021, 7, 8),
                              datetime.datetime(2021, 7, 9), datetime.datetime(2021, 7, 12),
                              datetime.datetime(2021, 7, 12), datetime.datetime(2021, 7, 14),
                              datetime.datetime(2021, 7, 14), datetime.datetime(2021, 7, 28),
                              datetime.datetime(2021, 7, 27), datetime.datetime(2021, 7, 27),
                              datetime.datetime(2021, 7, 27), datetime.datetime(2021, 7, 27),
                              datetime.datetime(2021, 8, 2), datetime.datetime(2021, 8, 10),
                              datetime.datetime(2021, 8, 10), datetime.datetime(2021, 8, 16),
                              datetime.datetime(2021, 8, 17), datetime.datetime(2021, 8, 17),
                              datetime.datetime(2021, 8, 19), datetime.datetime(2021, 8, 20),
                              datetime.datetime(2021, 8, 25), datetime.datetime(2021, 8, 31),
                              datetime.datetime(2021, 8, 31), datetime.datetime(2021, 8, 30),
                              datetime.datetime(2021, 9, 7), datetime.datetime(2021, 9, 7),
                              datetime.datetime(2021, 9, 9), datetime.datetime(2021, 9, 13),
                              datetime.datetime(2021, 9, 13), datetime.datetime(2021, 9, 13),
                              datetime.datetime(2021, 9, 27), datetime.datetime(2021, 9, 27),
                              datetime.datetime(2021, 9, 27), datetime.datetime(2021, 9, 30),
                              datetime.datetime(2021, 9, 30), datetime.datetime(2021, 9, 30),
                              datetime.datetime(2021, 9, 30), datetime.datetime(2021, 9, 4),
                              datetime.datetime(2021, 9, 4), datetime.datetime(2021, 9, 4),
                              datetime.datetime(2021, 9, 4), datetime.datetime(2021, 10, 6),
                              datetime.datetime(2021, 10, 6), datetime.datetime(2021, 10, 6),
                              datetime.datetime(2021, 10, 11), datetime.datetime(2021, 10, 15),
                              datetime.datetime(2021, 10, 29), datetime.datetime(2021, 11, 1),
                              datetime.datetime(2021, 11, 1), datetime.datetime(2021, 11, 18),
                              datetime.datetime(2021, 11, 22), datetime.datetime(2021, 1, 26)]}
# Pandas engaged
ticker_df_long = pd.DataFrame(long_ticker_info, columns=['Symbol', 'Target', 'Date'])
ticker_df_short = pd.DataFrame(short_ticker_info, columns=['Symbol', 'Target', 'Date'])
# print('Symbol = {}\nTarget = {}\nDate = {}'.format(len(short_ticker_info['Symbol']),
#                                                    len(short_ticker_info['Target']),
#                                                    len(short_ticker_info['Date'])))

# get ticker info from yfinance
get_ticker_data(ticker_df_long, directory)
get_ticker_data(ticker_df_short, directory)

# check for what trades hit the PT eventually
long_target_hit(ticker_df_long, directory)
short_target_hit(ticker_df_short, directory)

# To do -
# * add way to manually add tickers,pt,date so it isnt hard coded in.
# * idea - for hits take entry date, stop loss, pt, and see if there is a
#          pattern to when PT was hit. did it double dip into entry and stop
#          before hitting PT ?
# * define how one specifies the ticker to look up plus price target.
exit()
