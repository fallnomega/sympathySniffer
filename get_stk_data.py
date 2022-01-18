import os
import yfinance as yf


def get_ticker_data(tickers, directoryz):
    for ind in tickers.index:
        if not os.path.exists(directoryz):
            os.makedirs(directoryz)
        if not os.path.exists('{}/{}.csv'.format(directoryz, tickers['Stock Symbol'][ind])):
            try:
                df = yf.download(tickers['Stock Symbol'][ind], period='2y', interval='1d')
                df.dropna(inplace=True)
                df["Symbol"] = tickers['Stock Symbol'][ind]
                df.to_csv('{}/{}.csv'.format(directoryz, tickers['Stock Symbol'][ind]))

            except Exception as ex:
                print('Error:', ex)
        else:
            print('-> Already have {}.csv file, skipping'.format(tickers['Stock Symbol'][ind]))

