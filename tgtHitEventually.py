#to see if picks eventually hit based on choices you or others took in the past
import os
import yfinance as yf
import pandas as pd
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
    for ticker,pt in tickers.items():
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists('{}/{}.csv'.format(directory,ticker)):
            try:

                print('Getting data for: {}'.format(ticker))
                # print price_target
                df = yf.download(ticker , period='2y', interval='1d')
                df.dropna(inplace=True)
                df["Symbol"] = ticker
                df.to_csv('{}/{}.csv'.format(directory,ticker))

            except Exception as ex:
                print('Error:', ex)
        else:
            print('-> Already have {} file so skipping'.format(ticker))

#determine if short or long
#long - determine if it ever hit the PT
def longTargethit(tickers,directory):
    for ticker,pt in tickers.items():
        print ('Opening {}.csv'.format(ticker))
        print('Parsing data to see if {} ever hit ${}'.format(ticker,pt))
        data = pd.read_csv('{}/{}.csv'.format(directory,ticker))
        # print data
        # print data.Close
        for ind in data.index:
            if data['High'][ind] >= pt:
                print ('{} PT hit: \nDate - {}    High - {}'.format(data['Symbol'][ind],data['Date'][ind],data['High'][ind]))
        print ('\n\n')

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



ticker_pt = {'AAPL':180,'TSLA':1210}
directory = 'targetHitEventually'

get_ticker_data(ticker_pt,directory)
longTargethit(ticker_pt,directory)

# print ticker_pt['ticker']
# print ticker_pt['price_target']
# longTargethit(ticker_pt,'targetHitEventually')