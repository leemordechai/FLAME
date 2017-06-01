import pandas as pd
import numpy as np
import datetime as dt
from brit_conv import OSGB36toWGS84	# requires an additional file
import requests, json

brit_coin_finds = pd.read_excel('Consolidated Reece 16+ hoard details_with numbers.xlsx')
brit_coin_groups = pd.read_csv('Roman hoards content summaries_short.csv')

#print(brit_coin_finds.columns)
#print(brit_coin_groups.columns)

cols = ['hoard_id', 'coin_group_id', 'start_year', 'end_year', 'denomination', 'num_coins', 'mint', 'created']
coin_groups = pd.DataFrame(columns=cols)

cols_finds = ['hoard_id', 'endDate', 'type_find', 'hoard?', 'excavation?', 'single?', 'num_coins', 'num_known_coins', 'num_unknown_coins', 'year_found',
	'year_end_found', 'comments', 'lat', 'long', 'certainty', 'owner', 'created']
coin_finds = pd.DataFrame(columns=cols_finds)
#print(coin_groups.head())

# this function verifies that the number of reported identified coins found in the hoard
# is the same as the sum of the identified number of coin groups
def testing_database_connections():
	# this block creates a new DF, datatest, and initializes the sum of its coin groups to 0
	list_of_fields = ['old_findID', 'QuantityCoins', 'Denomination_KnownTotal', 'Denomination_UnknownTotal']
	datatest = brit_coin_finds[list_of_fields]
	datatest['sum_coin_groups'] = 0
	datatest.set_index('old_findID', inplace=True)
	
	# this sums up all the coin groups and puts the result in hoards, a dict
	hoards = {}
	for i in range(len(brit_coin_groups)):
		if brit_coin_groups.hoard.iloc[i] in hoards:
			hoards[brit_coin_groups.hoard.iloc[i]] += brit_coin_groups.quantity.iloc[i]
		else:
			hoards[brit_coin_groups.hoard.iloc[i]] = brit_coin_groups.quantity.iloc[i]
	
	# this block updates the datatest based on the dict we've just created
	hoard_list = datatest.index.tolist()
	temp_hoards = hoards.copy()		#This begins with 2424 hoards
	for i in temp_hoards:
		if i in hoard_list:
			try:
				datatest.set_value(i, 'sum_coin_groups', hoards[i])
			except:
				print('Hoard with no datable coin groups:', i, hoards[i])
			del hoards[i]
	
	# gives feedback to user
	#print(datatest[datatest.sum_coin_groups != 0])
	print('Overall {} hoards with {} coins.'.\
			format(len(hoard_list), datatest['QuantityCoins'].sum()))		
			# 431455 coins in 820 relevant coin groups
	print('{} hoards with {} coins are datable.'.\
			format(len(datatest[datatest.sum_coin_groups != 0]), datatest['sum_coin_groups'].sum()))
			# 323223 coins in 692 datable coin groups
	print(len(hoards))	# 1684 hoards remain here, meaning they are not relevant
	#print(datatest[datatest.Denomination_KnownTotal + datatest.Denomination_UnknownTotal != datatest.QuantityCoins])
	# 1 hoard has an issue here
	#print(len(datatest[datatest.sum_coin_groups != datatest.QuantityCoins]),
	#	datatest[datatest.sum_coin_groups != datatest.QuantityCoins])
	# 259 hoards have unknown denominations


coin_groups['hoard_id'] = brit_coin_groups['hoardID']
coin_groups['coin_group_id'] = brit_coin_groups['id']
coin_groups['start_year'] = brit_coin_groups['fromDate']
coin_groups['end_year'] = brit_coin_groups['toDate']
coin_groups['denomination'] = brit_coin_groups['denomination']
coin_groups['num_coins'] = brit_coin_groups['quantity']
coin_groups['mint'] = brit_coin_groups['mint']
coin_groups['created'] = dt.datetime.now()

coin_finds['hoard_id'] = brit_coin_finds['GIS_ID']
coin_finds['type_find'] = brit_coin_finds['DatasetQual']
coin_finds['endDate'] = brit_coin_finds['toTerminalYear']
coin_finds['num_coins'] = brit_coin_finds['QuantityCoins']
coin_finds['num_known_coins'] = brit_coin_finds['Denomination_KnownTotal']
coin_finds['num_unknown_coins'] = brit_coin_finds['Denomination_UnknownTotal']
coin_finds['year_found'] = brit_coin_finds['YearFound1']
coin_finds['year_end_found'] = brit_coin_finds['YearFound2']
coin_finds['comments'] = brit_coin_finds['description']
coin_finds['created'] = dt.datetime.now()
coin_finds['owner'] = 'PAS UK Finds'
coin_finds['hoard?'] = 'hoard'
coin_finds.loc[coin_finds.type_find == 'AC_Excavated', 'excavation?'] = 'excav'

##### sorting coordinates #####
geourl = "https://api.postcodes.io/places?q="
parishes = {"Savernake":"Cadley"}
districts = {'Bath and North East Somerset': "Bath", "City of Bristol":"Bristol", "Derbyshire Dales":"Longcliffe",
			"North Dorset":"Shillingstone", "Dorset":"Dorchester", "Weymouth and Portland":"Weymouth", 
			"Gravesham":"Cobham", "Medway":"Chattenden", "King's Lynn and West Norfolk":"King's Lynn",
			"Wiltshire":"Shrewton"}
counties = {'Buckinghamshire': 'Aylesbury', "Norfolk":"Norwich", "Dorset":"Dorchester",}
for i in range(len(coin_finds)):	# convers the UK geographic system to coordinates
	#print(str(brit_coin_finds.iloc[i]['easting']), str(brit_coin_finds.iloc[i]['northing']))
	if(brit_coin_finds.iloc[i]['easting'] == brit_coin_finds.iloc[i]['easting']):
		temp = OSGB36toWGS84(brit_coin_finds.iloc[i]['easting'], brit_coin_finds.iloc[i]['northing'])
		coin_finds['lat'].iloc[i] = temp[0]
		coin_finds['long'].iloc[i] = temp[1]
	else:	# get an estimate about the location
		if (brit_coin_finds.iloc[i]['parish'] == brit_coin_finds.iloc[i]['parish']):
			if brit_coin_finds.iloc[i]['parish'] in parishes: add = parishes[brit_coin_finds.iloc[i]['parish']]
			else: add = brit_coin_finds.iloc[i]['parish']
		elif(brit_coin_finds.iloc[i]['district'] == brit_coin_finds.iloc[i]['district']):
			if brit_coin_finds.iloc[i]['district'] in districts: add = districts[brit_coin_finds.iloc[i]['district']]
			else: add = brit_coin_finds.iloc[i]['district']
		elif(brit_coin_finds.iloc[i]['county'] == brit_coin_finds.iloc[i]['county']):
			if brit_coin_finds.iloc[i]['county'] in counties: add = counties[brit_coin_finds.iloc[i]['county']]
			else: add = brit_coin_finds.iloc[i]['county']
		else:
			add = "Whalley"	# center of UK
		r = requests.get(geourl + add)
		temp = json.loads(r.text)
		try:
			coin_finds['lat'].iloc[i] = temp['result'][0]['latitude']
			coin_finds['long'].iloc[i] = temp['result'][0]['longitude']
		except:
			print(add)
	

brit_coin_finds['certainty'] = 'highest'
brit_coin_finds.loc[pd.isnull(brit_coin_finds.parish), 'certainty'] = 'lower'
brit_coin_finds.loc[pd.isnull(brit_coin_finds.county), 'certainty'] = 'lowest'
coin_finds['certainty'] = brit_coin_finds['certainty']




	


#have_good_dates = coin_groups[coin_groups.end_year > 325]	# works
#no_dates = coin_groups[pd.isnull(coin_groups['end_year'])] # works
have_bad_dates = coin_groups[coin_groups.end_year < 325]	# works

list_of_bad = have_bad_dates.index.tolist()	# prepare for filtering out
coin_groups = coin_groups.drop(list_of_bad)	# drop all irrelevant rows

irrelevant_denominations = ['Radiate (antoninianus)', 'Sestertius', 'Denarius (Empire)', 
							'Denarius (Roman Republic)', 'Dupondius', 'Quinarius',
							'As (Roman Republic)', 'Quadrans (Roman Republic)', 'Quadrans',
							'Sestertius (Roman Republic)', 'Dupondius or as',
							'Sestertius, dupondius or as', 'Q radiate']
for irr_den in irrelevant_denominations:
	print('{} of "{}" removed.'.format(len(coin_groups[coin_groups.denomination == irr_den]), irr_den))
	coin_groups = coin_groups[coin_groups.denomination != irr_den]

print('Overall, {} coin groups remain in the database and ready for import'.format(len(coin_groups)))
print('This is the list of coin denominations that remains in the database: {}'.format(coin_groups.denomination.unique()))
print()
coin_groups.to_csv('coin_groups.csv')

coin_finds.to_csv('coin_finds.csv')

#testing_database_connections()