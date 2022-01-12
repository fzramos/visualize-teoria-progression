# Experimenting with Pandas Grouper for User Input
# This will let me group records by different lengths of time more easily
# TODO: After grouper, sum "Correct" and "Error" columns.
# Note: will be filtering by "Exercises" column in future so sum that as well
import pandas as pd

df = pd.read_csv('./assets/historical_stats.csv',
                parse_dates = ['Date/time'])

print(df.head())

# Grouper required the Datetime column to be the index
df_date = df.set_index('Date/time')

df_count_day = df2.groupby(pd.Grouper(freq='D')).size()
print(df_count_day)

df_count_week = df2.groupby(pd.Grouper(freq='W')).size()
print(df_count_week)

df_count_month = df2.groupby(pd.Grouper(freq='M')).size()
print(df_count_month)