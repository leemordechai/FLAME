import pandas as pd
import numpy as np
import datetime as dt
from brit_conv import OSGB36toWGS84	# requires an additional file
import requests, json

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

def setFindsGeo():		# sets coordinates for all coin finds
	##### sorting coordinates #####
	geourl = "https://api.postcodes.io/places?q="

	# manual fixes for areas that aren't found by the geolocator service
	parishes = {"Savernake":"Cadley"}
	districts = {'Bath and North East Somerset': "Bath", "City of Bristol":"Bristol", "Derbyshire Dales":"Longcliffe",
				"North Dorset":"Shillingstone", "Dorset":"Dorchester", "Weymouth and Portland":"Weymouth", 
				"Gravesham":"Cobham", "Medway":"Chattenden", "King's Lynn and West Norfolk":"King's Lynn",
				"Wiltshire":"Shrewton"}
	counties = {'Buckinghamshire': 'Aylesbury', "Norfolk":"Norwich", "Dorset":"Dorchester"}

	# gets the coordinates for the places listed, at varying levels of precision
	for i in range(len(coin_finds)):	# convers the UK geographic system to coordinates
		print("Error!!!")
		if(brit_coin_finds['easting'].iloc[i] == brit_coin_finds['easting'].iloc[i]):
			temp = OSGB36toWGS84(brit_coin_finds['easting'].iloc[i], brit_coin_finds['northing'].iloc[i])
			coin_finds['lat'].iloc[i] = temp[0]
			coin_finds['long'].iloc[i] = temp[1]
			
		else:	# get an estimate about the location based on the available data
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
				print(add)	# this should not print anything
		

	brit_coin_finds['certainty'] = 'highest'
	brit_coin_finds.loc[pd.isnull(brit_coin_finds.parish), 'certainty'] = 'lower'
	brit_coin_finds.loc[pd.isnull(brit_coin_finds.county), 'certainty'] = 'lowest'
	coin_finds['certainty'] = brit_coin_finds['certainty']

def year_limit(denom_list, denom, time):
	if denom in denom_list:
		if time == "start": return denom_list[denom][0]
		if time == "end": return denom_list[denom][1]
	else: 
		print(denom)
		return "irrelevant"


brit_coin_finds = pd.read_excel('Consolidated Reece 16+ hoard details_with numbers.xlsx')
#brit_coin_groups = pd.read_csv('Roman hoards content summaries_short.csv')
brit_coin_groups = pd.read_csv('testing_coin_groups.csv')

#print(brit_coin_finds.columns)
#print(brit_coin_groups.columns)

cols = ['hoard_id', 'coin_group_id', 'start_year', 'end_year', 'revised_start', 'revised_end', 'ruler', 'revised_ruler'
	'denomination', 'num_coins', 'mint', 'imported', 'created', 'updated']
coin_groups = pd.DataFrame(columns=cols)

cols_finds = ['hoard_id', 'endDate', 'type_find', 'hoard?', 'excavation?', 'single?', 'num_coins', 'num_known_coins', 'num_unknown_coins', 'year_found',
	'year_end_found', 'comments', 'lat', 'long', 'certainty', 'owner', 'created', 'imported']
coin_finds = pd.DataFrame(columns=cols_finds)
#print(coin_groups.head())


coin_groups['hoard_id'] = brit_coin_groups['hoardID']
coin_groups['coin_group_id'] = brit_coin_groups['id']
coin_groups['start_year'] = brit_coin_groups['fromDate']
coin_groups['end_year'] = brit_coin_groups['toDate']
coin_groups['denomination'] = brit_coin_groups['denomination']
coin_groups['num_coins'] = brit_coin_groups['quantity']
coin_groups['mint'] = brit_coin_groups['mint']
coin_groups['created'] = brit_coin_groups['created']
coin_groups['ruler'] = brit_coin_groups['ruler']
coin_groups['updated'] = brit_coin_groups['updated']
coin_groups['imported'] = dt.datetime.now()

coin_finds['hoard_id'] = brit_coin_finds['GIS_ID']
coin_finds['type_find'] = brit_coin_finds['DatasetQual']
coin_finds['endDate'] = brit_coin_finds['toTerminalYear']
coin_finds['num_coins'] = brit_coin_finds['QuantityCoins']
coin_finds['num_known_coins'] = brit_coin_finds['Denomination_KnownTotal']
coin_finds['num_unknown_coins'] = brit_coin_finds['Denomination_UnknownTotal']
coin_finds['year_found'] = brit_coin_finds['YearFound1']
coin_finds['year_end_found'] = brit_coin_finds['YearFound2']
coin_finds['comments'] = brit_coin_finds['description']
coin_finds['imported'] = dt.datetime.now()
coin_finds['owner'] = 'PAS UK Finds'
coin_finds['hoard?'] = 'hoard'
coin_finds.loc[coin_finds.type_find == 'AC_Excavated', 'excavation?'] = 'excav'

setFindsGeo()

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

# Removes all irrelevant rulers from the data frame
irrelevant_rulers = ["Julio-Claudian (uncertain)", "Caligula", "Claudius", "Vespasian", "Marcus Aurelius (as Augustus)",
	"Lucilla", "Antonine Empress, uncertain, 138-185", "Uncertain - 1st/2nd Century AD"]
for irr_ruler in irrelevant_rulers:
	coin_groups = coin_groups[coin_groups.ruler != irr_ruler]




# coin groups part
flame_denominations = pd.read_excel('Denominations.xlsx')
flame_mints = pd.read_excel('Mints.xlsx')
flame_rulers = pd.read_excel('Rulers.xlsx')

#coin groups - to do:
#	denomination - use a standardized name for these (but also keep the old name; use dictionary to translate).
# 	create update function to update only those entries that have been updated (as in the column)
ruler_list = {"House of Constantine":(307, 363), "House of Valentinian":(364,378), "House of Theodosius":(378, 408),
	"Magnentius":(350,353), "Uncertain (AD 260 - 402)":(260, 402)}
	#"Constantine I":(307,337), "Julian":(361, 363), "Gratian":(367,383)}
for i in range(len(flame_rulers)):
	ruler_list[flame_rulers['RulerName'].iloc[i]] = (flame_rulers['RulerStartYear'].iloc[i],flame_rulers['RulerEndYear'].iloc[i])

denomination_dates = {"Nummus (AE 1 - AE 4)":(302, 402),	# based on existing entries
					"Radiate or nummus":(260, 402),			# based on existing entries (/w corrections)
					"Siliqua":(360, 402),					# based on existing entries
					"Uncertain (copper alloy)":(-100, 410),	# one such entry
					"Uncertain (silver)":(-100, 410),		# one such entry
					"Unspecified ruler (contemporary copy)":(-100, 410) # one such entry
					}
mint_conversion = {"Trier": "Colonia Augusta Treverorum", "Lyon": "Lugdunensium", "Arles": "Arelato", "Rome": "Roma",
			"Thessalonica": "Thessalonika", "Siscia": "Siscia", "Aquileia": "Aquileia", "Milan": "Mediolanum"}


coin_groups['revised_start'] = coin_groups['start_year']
coin_groups['revised_end'] = coin_groups['end_year']
for i in range(len(coin_groups)):
	# this fills in the missing years, if relevant (checks ruler first, then denomination)
	try:	
		if(coin_groups.iloc[i]['revised_start'] != coin_groups.iloc[i]['revised_start']):
			if coin_groups['ruler'].iloc[i] == 'Unspecified ruler (contemporary copy)':
				temp = year_limit(denomination_dates, coin_groups['denomination'].iloc[i], "start")
				if temp != "irrelevant": coin_groups['revised_start'].iloc[i] = temp
			else: coin_groups['revised_start'].iloc[i] = ruler_list[coin_groups['ruler'].iloc[i]][0]
		if(coin_groups.iloc[i]['revised_end'] != coin_groups.iloc[i]['revised_end']):
			if coin_groups['ruler'].iloc[i] == 'Unspecified ruler (contemporary copy)':
				temp = year_limit(denomination_dates, coin_groups['denomination'].iloc[i], "end")
				if temp != "irrelevant": coin_groups['revised_end'].iloc[i] = temp
			else: coin_groups['revised_end'].iloc[i] = ruler_list[coin_groups['ruler'].iloc[i]][1]
	except:
		print("Error: Unknown ruler: {}".format(coin_groups.iloc[i]['ruler']))	# this should print nothing if working as intended
	
	# this section standardizes the mint names to those in FLAME's database
	try:
		if coin_groups['mint'].iloc[i] == coin_groups['mint'].iloc[i]:
			try:
				coin_groups['mint'].iloc[i] = mint_conversion[coin_groups['mint'].iloc[i]]
			except:
				print("Error: Unknown mint: {}".format(coin_groups['mint'].iloc[i]))	# this should print nothing if working as intended
	except:
		continue


coin_groups.to_csv('coin_groups.csv')

coin_finds.to_csv('coin_finds.csv')

#testing_database_connections()