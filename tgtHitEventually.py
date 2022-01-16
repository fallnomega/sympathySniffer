#to see if picks eventually hit based on choices you or others took in the past
import datetime
import os
import yfinance as yf
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

from collections import Counter
import csv
import glob
import operator
import openpyxl

#define how one specifies the ticker to look up plus price target.
#get ticker data
#pull date, current price, dates high, and dates low info from data
# data result example calling for AAPL:
#|Date|Adj Close|Close|High||Low|Open|Volume|Symbol
#|1/15/20|76.69576263|77.83499908|78.875|77.38749695|77.96250153|121923600|AAPL
#|1/16/20|77.65648651|78.80999756|78.92500305|78.02249908|78.39749908|108829200|AAPL

def get_ticker_data(tickers,directory):
    for ind in tickers.index:
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists('{}/{}.csv'.format(directory,tickers['Symbol'][ind])):
            try:

                print('Getting data for: {}'.format(tickers['Symbol'][ind]))
                # print price_target
                df = yf.download(tickers['Symbol'][ind] , period='2y', interval='1d')
                df.dropna(inplace=True)
                df["Symbol"] = tickers['Symbol'][ind]
                df.to_csv('{}/{}.csv'.format(directory,tickers['Symbol'][ind]))

            except Exception as ex:
                print('Error:', ex)
        else:
            print('-> Already have {}.csv file so skipping'.format(tickers['Symbol'][ind]))

#determine if short or long
#long - determine if it ever hit the PT
def longTargethit(tickers,directory):
    hits = 0
    for ind in tickers.index:
        print ('Opening {}.csv'.format(tickers['Symbol'][ind]))
        print('Parsing data to see if {} ever hit ${}'.format(tickers['Symbol'][ind],tickers['Target'][ind]))
        data = pd.read_csv('{}/{}.csv'.format(directory,tickers['Symbol'][ind]))
        tickers['Date'][ind] = pd.to_datetime(tickers['Date'][ind], errors='coerce')

        for indy in data.index:
            data['Date'][indy] = pd.to_datetime(data['Date'][indy], errors='coerce')

            if data['High'][indy] >= tickers['Target'][ind] and data['Date'][indy] >= tickers['Date'][ind]:
                print ('''
                Ticker = {}
                Entry Date = {}
                PT = {}
                PT hit on {} and had a high of {}
                '''.format(data['Symbol'][indy],tickers['Date'][ind],tickers['Target'][ind],data['Date'][indy],data['High'][indy]))
                hits = hits+1
                break
            continue

        print ('hits total = {} \n out of a total of {} ideas.\n\n'.format(hits,len(tickers)))

    return 0

#short - determine if it ever hit the PT
# def shortTargethit(ticker):
#     print('Looking to see if there are sympathy plays for: {}'.format(ticker))
#     df = pd.read_excel('sector_final_list.xlsx')
#     target = df[(df['Symbol'] == ticker)]
#     target_list = df.values.tolist()
#     sector = target['Sector'].values[0]
#     # print (sector)
#     list_dates = target.values.tolist()
#     same_list_results = list()
#     diff_sector_list = list()
#
#     for row in list_dates:
#         # print (row[3])
#         for row_df in target_list:
#             if row[3] == row_df[3] and sector == row_df[9]:
#                 # print ('SAME SECTOR - Date: {} | Symbol: ${} | Volume: {} | Open vs HOD percent difference: {} %'.format(row_df[3],row_df[10],row_df[11], round(row_df[8], 2)))
#                 same_list_results.append(row_df[10])
#     # print (list_results)
#     same_sector_count = Counter(same_list_results)
#     print ("Same Sector count:\n {}\n\n".format(same_sector_count))
#
#     for row in list_dates:
#         for row_df in target_list:
#             if row[3] == row_df[3]:
#                 # print ('CROSS SECTOR - Date: {} | Symbol: ${} | Volume: {} | Open vs HOD percent difference: {} % | Sector: {}'.format(row_df_dif_sector[3],row_df_dif_sector[10],row_df_dif_sector[11], round(row_df_dif_sector[8], 2),row_df_dif_sector[9]))
#                 diff_sector_list.append(row_df[10])
#     diff_sector_count = Counter(diff_sector_list)
#
#     print("Check cross sector potential sympathy plays :\n {}".format(diff_sector_count))
#
#
#
#
#
#     return 0



ticker_pt = {'AAL':20, 'VISL':2.3, 'SHWZ':2.5, 'AMD':91.76, 'ADMP':2, 'azrx':2, 'pltr':40, 'tsla':870, 'AIKI':2.62, 'AESE':3.5, 'ELYS':9.49, 'SPY':400, 'AAL':10.11, 'NIO':70, 'AAPL':145, 'AMC':16, 'AMC':17, 'NIO':60, 'MCD':210, 'FB':270, 'AEP':90, 'SNOW':300, 'DKNG':70, 'spce':55, 'spce':58, 'amzn':3500, 'nndm':20, 'ZM':400, 'DVAX':6.44, 'LODE':4, 'PHUN':4, 'INAQ':24.95, 'AACG':6, 'NFLX':560, 'AMD':90, 'JNJ':170, 'spce':60, 'nio':65, 'dkng':65, 'xpev':53, 'uber':65, 'ko':55, 'DIS':189.39, 'TTWO':214.39, 'SQ':264.69, 'ZAGG':5.5, 'LANC':230, 'sndl':2, 'ENBL':6.15, 'gsat':2.1, 'spce':60, 'IGC':3.1, 'EXPR':3.27, 'NXTD':3.4, 'SPCE':57.5, 'nxtd':3, 'pltr':40, 'MYT':4, 'ATIF':1.56, 'DPW':7.85, 'glw':39.39, 'nio':63.1, 'sckt':12.167, 'yell':9, 'CBAT':9.5, 'CBAT':9, 'MYT':7, 'SOLO':9.05, 'TLRY':29.61, 'GE':12.9, 'CLSN':3.5, 'AAL':21.58, 'YELL':9, 'U':106, 'OCGN':9.82, 'WKHS':18, 'NVDA':600, 'NTCO':20, 'CEF':20, 'SCKT':16.09, 'EBON':10.4, 'AQUA':28.62, 'SOS':9.99, 'XTNT':4, 'DKNG':75, 'WMT':133, 'SOS':9, 'CHFS':11.8, 'HTBX':9.99, 'LYFT':65, 'OCGN':12.21, 'LYFT':61.8, 'BRQS':2, 'PBR':8.15, 'MAC':15.89, 'SPXU':31, 'PBR':8.15, 'BAC':39.84, 'SQQQ':20, 'QQQ':315, 'SPY':400, 'lyft':70, 'WMT':135, 'COST':324, 'XPEV':40, 'SRNE':9.75, 'T':32.5, 'IBM':135, 'PTON':25, 'BLDP':114, 'LFMD':18.83, 'BAC':235, 'LFMD':23, 'XELA':5, 'QS':55, 'BAC':240, 'SNAP':62.56, 'PYPL':264.54, 'GTT':3.06, 'ENVB':8, 'AMC':13.5, 'ENTX':6.1, 'JMIA':4, 'MARA':55.32, 'AYX':93.91, 'DFEN':42.05, 'DOCU':286.32, 'LFMD':23, 'TLRY':40, 'K':65, 'TLT':150, 'TLT':129.68, 'cidm':2.61, 'cigx':8.1, 'JUVAF':1.2, 'REI':1, 'STT':15, 'T':33, 'TLT':2, 'U':118, 'SEAC':2.08, 'TSIA':12.48, 'WKEY':21, 'X':3.2, 'DISCA':47.5196, 'NIO':43.06, 'PFMT':2.6, 'YVR':5.02, 'GDDY':90, 'NPA':15, 'RIOT':60, 'FTFT':9.39, 'VIAC':45, 'RAIL':9.32, 'PMFT':2.61, 'PHUN':2.66, 'PAVM':8, 'sfet':2, 'VERY':25, 'AFMD':10.29, 'FEYE':25, 'TENX':2.39, 'MDT':130, 'pbts':3.19, 'CVS':90, 'CVS':88, 'KYMR':70, 'CIDM':2.1, 'ADMP':1.5, 'HUT':5.91, 'DPRO':4.5, 'DPRO':4, 'VXRT':11, 'SOFI':20, 'AUPH':16, 'ARRY':23, 'PLTR':28, 'GNLN':3.6, 'DPRO':6, 'VXRT':10.5, 'COIN':304.99, 'AYX':90, 'AUPH':12.88, 'ARRY':23, 'LTCH':11.75, 'BTBT':20, 'SRPT':100, 'OGI':3.45, 'ABNB':165, 'BTBT':20, 'SQQQ':9, 'SLV':30, 'T':31, 'CTRM':5, 'SLV':30, 'RIDE':8.5, 'LQTM':0.275, 'ATIF':8, 'MDIA':12.95, 'LOW':220, 'NURO':20, 'TGT':4, 'IPOF':11.15,}
directory = 'targetHitEventually'
ticker_info = {'Symbol': ['AAL', 'VISL', 'SHWZ', 'AMD'],
        'Target': [20, 2.3, 2.5, 91.97],
        'Date': [datetime.datetime(2021,01,15), datetime.datetime(2021,01,15), datetime.datetime(2021,01,19), datetime.datetime(2021,02,04)]}
ticker_df = pd.DataFrame(ticker_info, columns=['Symbol','Target','Date'])

get_ticker_data(ticker_df,directory)
longTargethit(ticker_df,directory)

# print ticker_pt['ticker']
# print ticker_pt['price_target']
# longTargethit(ticker_pt,'targetHitEventually')