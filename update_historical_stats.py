import pandas as pd

def update_historical_stats(new_stats_df):
    """
        As Teoria only keeps records of the last 7 days of trainings, this
        function adds the new records scraped from Teoria add appends
        them to an existing persistent csv file with previous days' records
        excluding any duplicates
        Input: dataframe
        Output: none
    """
    historic_df = pd.read_csv('./assets/historical_stats.csv',
                    parse_dates = ['Date/time']
                    )
    updated_historic_df = pd.concat([new_stats_df, historic_df]).drop_duplicates().reset_index(drop=True)
    updated_historic_df = updated_historic_df.sort_values(['Date/time'], ascending=True)
    updated_historic_df.to_csv('./assets/historical_stats.csv', index=False)
    print('New Teoria exercise statistics combined with historical statistics')

if __name__ == '__main__':
    new_stats_df = pd.read_csv('assets/stats.csv',
                parse_dates = ['Date/time']
                )
    update_historical_stats(new_stats_df)