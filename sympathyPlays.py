#panda is data analysis lib
import pandas as pd
from collections import Counter

import xlrd


def getPotentialSympathy(ticker):
    print('Looking to see if there are sympathy plays for: {}'.format(ticker))
    df = pd.read_excel('sector_final_list.xlsx')
    target = df[(df['Symbol'] == ticker)]
    target_list = df.values.tolist()
    sector = target['Sector'].values[0]
    # print (sector)
    list_dates = target.values.tolist()
    same_list_results = list()
    diff_sector_list = list()

    for row in list_dates:
        # print (row[3])
        for row_df in target_list:
            if row[3] == row_df[3] and sector == row_df[9]:
                # print ('SAME SECTOR - Date: {} | Symbol: ${} | Volume: {} | Open vs HOD percent difference: {} %'.format(row_df[3],row_df[10],row_df[11], round(row_df[8], 2)))
                same_list_results.append(row_df[10])
    # print (list_results)
    same_sector_count = Counter(same_list_results)
    print ("Same Sector count:\n {}\n\n".format(same_sector_count))

    for row in list_dates:
        for row_df in target_list:
            if row[3] == row_df[3]:
                # print ('CROSS SECTOR - Date: {} | Symbol: ${} | Volume: {} | Open vs HOD percent difference: {} % | Sector: {}'.format(row_df_dif_sector[3],row_df_dif_sector[10],row_df_dif_sector[11], round(row_df_dif_sector[8], 2),row_df_dif_sector[9]))
                diff_sector_list.append(row_df[10])
    diff_sector_count = Counter(diff_sector_list)

    print("Check cross sector potential sympathy plays :\n {}".format(diff_sector_count))





    return 0

#Insert ticker you want potential sympathy plays for.
ticker = input('Ticker to look up :')
ticker= ticker.upper()
try:
    getPotentialSympathy(ticker)
except Exception as ex:
    print('Error:', ex)