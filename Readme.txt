Run this first ..... sympathySniffer:
Finds stocks that ran together over a 3 year period. They may not actually run together but
this should narrow your results down when looking for stocks that run together.
Pulls data from YFinance, combines the ticker spreadsheets into one master per area of the sector
or industry, removes the ones with under 3 mil volume for the day + less than 10% gain on the day.

sympathyPlays:
Queries all in one final file; created by the sympathySniffer.py script,  to see what tickers that also ran with the ticker you specify.
Specified ticker hard coded in rightnow but will add user input prompt soon. This is still in
Alpha/Beta and not the most efficient nor elegant but it gets the job done.

Runs off Python and libraries needed are :

pandas
collections -> Counter
yfinance
bs4
pickle
requests
os
csv
glob
pandas
operator
openpyxl