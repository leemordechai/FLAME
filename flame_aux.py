# this script reads two large files and saves their entries which do not appear in the second two 
# large files as 'additional' files. This product is used in flame.py

import pandas as pd

coin_summary = pd.read_excel('CoinSummary.xlsx')
hoards = pd.ExcelFile('HoardsTableForRory.xlsx')

hoards_table = hoards.parse(9)
for i in range(9):
    hoards_table = pd.concat([hoards_table, hoards.parse(i)])
#hoards_table.sort_values('GIS_ID')

len(coin_summary) # 26788, indices read 26868
all_coin_groups_numbers = set(coin_summary.id.values)
print(len(all_coin_groups_numbers)) # 26788 - meaning no duplicates here

brit_imported_coin_finds = pd.read_excel('Consolidated Reece 16+ hoard details_with numbers.xlsx')
brit_imported_coin_groups = pd.read_csv('Roman hoards content summaries_short.csv')
print(len(brit_imported_coin_finds)) # 820
len(brit_imported_coin_groups) # 25826

for i in range(len(brit_imported_coin_finds)):
    if brit_imported_coin_finds.iloc[i].GIS_ID in all_hoard_numbers:
        all_hoard_numbers.discard(brit_imported_coin_finds.iloc[i].GIS_ID)
print(len(all_hoard_numbers)) # 662, these are hoards not examined previously.

additional_hoards = hoards_table[hoards_table['GIS_ID'].isin(all_hoard_numbers)]
additional_hoards.head(1) # note that this has 179 columns compared to 82 in the brit_imported_coin_finds file

for i in range(len(brit_imported_coin_groups)):
    if brit_imported_coin_groups.iloc[i].id in all_coin_groups_numbers:
        all_coin_groups_numbers.discard(brit_imported_coin_groups.iloc[i].id)
print(len(all_coin_groups_numbers)) # 1148

additional_coin_finds = coin_summary[coin_summary['id'].isin(all_coin_groups_numbers)] # 1148 in length
additional_coin_finds.head()

additional_hoards.to_csv('additional_hoards.csv')
additional_coin_finds.to_csv('additional_coin_groups.csv')