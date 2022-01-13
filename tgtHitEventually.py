#to see if picks eventually hit based on choices you or others took in the past
import os
import yfinance as yf
import pandas as pd
import csv
import glob
import operator
import openpyxl

#define how one specifies the ticker to look up plus price target.
#get ticker data
def get_ticker_data(tickers,directory):
    for x in tickers:
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists('{}}/{}.csv'.format(directory,x)):
            try:

                print('Getting data for: ' + x)
                df = yf.download(x , period='2y', interval='1d')
                df.dropna(inplace=True)
                df["Symbol"] = x
                df["PercentIncrease_High_Open"] = df['High']*100 / df['Open'] -100
                df["Sector"] = '{}'.format(directory)
                df.to_csv('{}}/{}.csv'.format(directory,x))

            except Exception as ex:
                print('Error:', ex)
        else:
            print('-> Already have {} file so skipping'.format(x))

#pull date, current price, dates high, and dates low info from data
#determine if short or long
#long - determine if it ever hit the PT
#short - determine if it ever hit the PT

