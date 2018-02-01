import pandas as pd
import numpy as np
import datetime as dt

ths = pd.read_csv('THS.csv', index_col='ID')

# function to convert denominations to the standard nummi notation
def convert_denomination(df):
	di = {'K':'20 nummi', 'IS':'16 nummi', 'M':'40 nummi', 'B':'2 nummi', 'A':'1 nummus', 'H':'8 nummi', 'I':'10 nummi', 'E':'5 nummi', 'D':'4 nummi'}
	df = df.replace({'Denomination':di})
	return df


# function to build the coin_finds dataframe
def setting_coin_finds(ths):
	cols_finds = ['hoard_id', 'name', 'startDate', 'endDate', 'type_find', 'hoard?', 'excavation?', 'single?', 'num_coins', 'num_known_coins', 'num_unknown_coins', 'year_found',
		'year_end_found', 'comments', 'lat', 'long', 'certainty', 'owner', 'created', 'imported']
	coin_finds = pd.DataFrame(columns=cols_finds)

	coin_finds['hoard_id'] = 'THS-' + (pd.Series(ths.index)-1).apply(str)
	coin_finds['name'] = ths['Location'] + ', ' + ths['Region'] + '(' + coin_finds['hoard_id'] + ')'
	coin_finds['startDate'] = ths['Date1']
	coin_finds['endDate'] = ths['Date2']
	coin_finds['hoard?'] = 0
	coin_finds['excavation?'] = 0
	coin_finds['single?'] = 1
	coin_finds['type_find'] = 'single find'
	coin_finds['num_coins'] = ths['Number']
	coin_finds['num_known_coins'] = ths['Number']
	coin_finds['num_unknown_coins'] = ths['Number']
	coin_finds['owner'] = 'Andrei Gandila'
	coin_finds['created'] = pd.Timestamp.now()
	coin_finds['imported'] = pd.Timestamp.now()
	coin_finds['comments'] = ths['Notes']
	#coin_finds = coin_finds.drop([0])

	return coin_finds


# function to set the coin_groups dataframe
def setting_coin_groups(ths):
	cols = ['hoard_id', 'coin_group_id', 'start_year', 'end_year', 'revised_start', 'revised_end', 'ruler', 'revised_ruler',
		'denomination', 'num_coins', 'mint', 'imported', 'created', 'updated']
	coin_groups = pd.DataFrame(columns=cols)

	coin_groups['hoard_id'] = 'THS-' + (pd.Series(ths.index)-1).apply(str)
	coin_groups['coin_group_id'] = coin_groups['hoard_id'] + '-1' # since these are all single finds
	coin_groups['start_year'] = ths['Date1']
	coin_groups['end_year'] = ths['Date2']
	coin_groups['revised_start'] = coin_groups['start_year']
	coin_groups['revised_end'] = coin_groups['end_year']
	coin_groups['ruler'] = 'placeholder'				# 31.1 need to correct this
	coin_groups['revised_ruler'] = coin_groups['ruler']
	coin_groups['denomination'] = ths['Denomination']
	coin_groups['num_coins'] = ths['Number']
	coin_groups['mint'] = 'Thessaloniki'
	coin_groups['imported'] = pd.Timestamp.now()	# this and the next two lines are identical because importing should be a one-off thing.
	coin_groups['created'] = pd.Timestamp.now()
	coin_groups['updated'] = pd.Timestamp.now()

	#coin_groups = coin_groups.drop([0])

	return coin_groups


ths = convert_denomination(ths)
print(len(setting_coin_finds(ths)))
print(len(setting_coin_groups(ths)))

#print(ths.head())