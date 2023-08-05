

import os
from sunpy.net import Fido, attrs as a
from sunpy.io.special import srs
import numpy as np
import pandas as pd


def srs_downloader(start_date, end_date, dwnld_dir):

    """ downloads NOAA Solar Region Summary """
    
    srs_search = Fido.search(a.Time(start_date, end_date), a.Instrument.srs_table)
    dwnld = Fido.fetch(srs_search, path = dwnld_dir, progress = True, overwrite = False)


def srs_new_sunspots(srs_dwnld_directory):

    """ compares srs data from previous days to current days to identify emergences of new sunspots,
    returns pandas data frame of new sunspots """
    
    srs_data = []
    for file_name in os.listdir(srs_dwnld_directory):
        if os.path.isfile(os.path.join(srs_dwnld_directory, file_name)):
            print(file_name)
            file_path = os.path.join(srs_dwnld_directory, file_name)
            srs_table = srs.read_srs(file_path)
            srs_table_df = srs_table.to_pandas()

            srs_table_df = srs_table_df[(srs_table_df['ID'] == 'I') | (srs_table_df['ID'] == 'IA')]

            srs_data.append(srs_table_df)
    

    file_list = os.listdir(srs_dwnld_directory)
    file_list = [file_name.rstrip("SRS.txt") for file_name in file_list]
    new_sunspots_data = []
    new_sunspots = []
    for i in range(len(srs_data) - 1):
        day = srs_data[i]
        next_day = srs_data[i + 1]

        new_sunspot = next_day[~next_day['Number'].isin(day['Number'])]

        new_sunspot_copy = new_sunspot.copy()
        date_observed = pd.to_datetime(file_list[i + 1])
        new_sunspot_copy['Date Observed'] = date_observed

        new_sunspots_data.append(new_sunspot_copy)
    
    new_sunspots_data = [df for df in new_sunspots_data if not df.empty]
    new_sunspots = pd.concat(new_sunspots_data, ignore_index = True)

    return new_sunspots



start_date = '2011-02-13'  
end_date = '2011-02-14'
srs_directory = 'C:\\Users\\Jjzar\\OneDrive\\Documents\\ASSURE\\ASSURE 2023\\Exploring the Unseen Sun\\srs_data\\2011-2022'

#srs_downloader(start_date, end_date, srs_directory)

sunspots = srs_new_sunspots(srs_directory)

print(sunspots)





# srs_data = []
# for file_name in os.listdir(srs_directory):
#     if os.path.isfile(os.path.join(srs_directory, file_name)):
#         file_path = os.path.join(srs_directory, file_name)
#         srs_table = srs.read_srs(file_path)
#         srs_table_df = srs_table.to_pandas()

#         srs_table_df = srs_table_df[(srs_table_df['ID'] == 'I') | (srs_table_df['ID'] == 'IA')]

#         srs_data.append(srs_table_df)




# file_list = os.listdir(srs_directory)
# file_list = [file_name.rstrip("SRS.txt") for file_name in file_list]
# new_sunspots_data = []
# for i in range(len(srs_data) - 1):
#     day = srs_data[i]
#     next_day = srs_data[i + 1]

#     new_sunspot = next_day[~next_day['Number'].isin(day['Number'])]
#     new_sunspot_copy = new_sunspot.copy()

#     date_observed = pd.to_datetime(file_list[i + 1])
#     new_sunspot_copy['Date Observed'] = date_observed

#     new_sunspots_data.append(new_sunspot_copy)


# new_sunspots_data = [df for df in new_sunspots_data if not df.empty]

# new_sunspots = pd.concat(new_sunspots_data, ignore_index =  True)

# print(new_sunspots)
# pd.set_option('display.max_columns', None)
# print(new_sunspots_copy)

