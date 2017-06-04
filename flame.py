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
		if(brit_coin_finds['easting'].iloc[i] == brit_coin_finds['easting'].iloc[i]):
			temp = OSGB36toWGS84(brit_coin_finds['easting'].iloc[i], brit_coin_finds['northing'].iloc[i])
			coin_finds.set_value(i, 'lat', temp[0])
			coin_finds.set_value(i, 'long', temp[1])
			
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
				coin_finds.set_value(i, 'lat', temp['result'][0]['latitude'])
				coin_finds.set_value(i, 'long', temp['result'][0]['longitude'])
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
brit_coin_groups = pd.read_csv('Roman hoards content summaries_short.csv')
#brit_coin_groups = pd.read_csv('testing_coin_groups.csv')

cols = ['hoard_id', 'coin_group_id', 'start_year', 'end_year', 'revised_start', 'revised_end', 'ruler', 'revised_ruler',
	'denomination', 'num_coins', 'mint', 'imported', 'created', 'updated']
coin_groups = pd.DataFrame(columns=cols)

cols_finds = ['hoard_id', 'endDate', 'type_find', 'hoard?', 'excavation?', 'single?', 'num_coins', 'num_known_coins', 'num_unknown_coins', 'year_found',
	'year_end_found', 'comments', 'lat', 'long', 'certainty', 'owner', 'created', 'imported']
coin_finds = pd.DataFrame(columns=cols_finds)

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
							'Sestertius (Roman Republic)', 'Dupondius or as', 'Double sestertius',
							'Sestertius, dupondius or as', 'Q radiate', 'As', 'Semis', 'Stater (gold)']
for irr_den in irrelevant_denominations:
	print('{} of "{}" removed.'.format(len(coin_groups[coin_groups.denomination == irr_den]), irr_den))
	coin_groups = coin_groups[coin_groups.denomination != irr_den]

print('Overall, {} coin groups remain in the database and ready for import'.format(len(coin_groups)))
print('This is the list of coin denominations that remains in the database: {}'.format(coin_groups.denomination.unique()))
print()

# Removes all irrelevant rulers from the data frame
irrelevant_rulers = ["Julio-Claudian (uncertain)", "Caligula", "Claudius", "Vespasian", "Marcus Aurelius (as Augustus)",
	"Lucilla", "Antonine Empress, uncertain, 138-185", "Uncertain - 1st/2nd Century AD", 'Licinius I', 
	'Diocletian', 'Constantius I', 'Maximian I', 'Galeria Valeria', 'Nero', 'Galba', 'Otho', 'Vitellius',
	'Titus', 'Trajan', 'Hadrian', 'Sabina', 'Nerva', 'Domitian', 'Antoninus Pius', 'Aelius Caesar', 'Maxentius',
	'Marciana', 'Maximinus Daia', 'Tetrarchic Ruler (uncertain issuer)', 'Faustina II', 'Caracalla', 'Philip I',
	'Philip II', 'Gordian III', 'Severus Alexander', 'Elagabalus', 'Uncertain - 1st-mid 3rd century', 'Probus',
	'Victorinus', 'Galerius', 'Divus Claudius (Official)', 'Aurelian', 'Gallienus (sole reign)', 
	'Salonina (sole reign of Gallienus)', 'Radiate, Uncertain Ruler 260-296', 'Balbinus', 'Licinius II']
for irr_ruler in irrelevant_rulers:
	coin_groups = coin_groups[coin_groups.ruler != irr_ruler]




########## coin groups part ##########
flame_denominations = pd.read_excel('Denominations.xlsx')
flame_mints = pd.read_excel('Mints.xlsx')
flame_rulers = pd.read_excel('Rulers.xlsx')

# setting conversions
ruler_list = {"House of Constantine":(307, 363), "House of Valentinian":(364,378), "House of Theodosius":(378, 408),
	"Magnentius":(350,353), "Uncertain (AD 260 - 402)":(260, 402), 
	'Uncertain - 4th century':(300, 399), 'Magnentius or Decentius': (350, 353),
	'Flavius Victor':(384, 388), 'Dalmatius':(335, 337)}
for i in range(len(flame_rulers)):
	ruler_list[flame_rulers.ix[i, 'RulerName']] = (flame_rulers['RulerStartYear'].iloc[i],flame_rulers['RulerEndYear'].iloc[i])

denomination_dates = {"Nummus (AE 1 - AE 4)": (302, 402),	# based on existing entries
					"Radiate or nummus": (260, 402),		# based on existing entries (/w corrections)
					"Siliqua": (360, 402),					# based on existing entries
					"Uncertain (copper alloy)":(-100, 410),	# one such entry
					"Uncertain (silver)": (-100, 410),		# one such entry
					"Unspecified ruler (contemporary copy)":(-100, 410), # one such entry
					"Nummus, uncertain ruler, c. 330-402": (300, 402)
					}
# order: 	mint name in UK database:mint name in FLAME
mint_conversion = {"Trier": "Colonia Augusta Treverorum", "Lyon": "Lugdunensium", "Arles": "Arelato", 
				"Rome": "Roma",	"Thessalonica": "Thessalonika", "Siscia": "Siscia", "Aquileia": "Aquileia", 
				"Milan": "Mediolanum", 'Amiens (Ambianum)': 'Ambianum', 'Nicomedia':'Nikomedia', 
				"Heraclea":"Heraclea", "London":"Londinium", "Antioch":"Antioch", "Pavia":"Pavia",
				"Cyzicus":"Kyzikos", 'Sirmium':'Sirmium', 'Constantinople':'Constantinople',
				"Ravenna":"Ravenna", "Alexandria":"Alexandria"}
# order: 	denomination in UK database:denomination name in FLAME
denomination_conversion = {'Nummus (AE 1 - AE 4)':"AE 1-4 (UK find)",	# new denomination (bronze)
						'Miliarensis':"miliarensis",
						'Siliqua': "siliqua",
						'Radiate or nummus':"radiate or nummus (UK find)", # new denomination (bronze)
						'Solidus':"solidus",
						'Half unit (silver)':"half unit", 	# new denomination (silver)
						'Unit (silver)': "unit",			# new denomination (silver)
						'Half-siliqua':"1/2 siliqua",
						'Tremissis':"tremissis",
						'Uncertain':"uncertain",
						'Uncertain (gold)':"uncertain (gold)",		# new denomination (gold)
						'Uncertain (silver)':"uncertain (silver)",	# new denomination (silver)
						'Uncertain (copper alloy)':"unidentified bronze coins"
						}
ruler_conversion = {'Honorius (emperor)': 'Honorius',
					'Nummus, uncertain ruler, c. 330-402': 'Unknown',
					'Uncertain': 'Unknown',
					'Uncertain - 4th century': 'Unknown',
					'Uninscribed': 'Unknown',
					'Unattributed': 'Unknown',
					'Dalmatius': 'Constantine I',
					'Magnentius or Decentius': 'Magnentius'

					}

coin_groups['revised_start'] = coin_groups['start_year']
coin_groups['revised_end'] = coin_groups['end_year']
coin_groups['revised_ruler'] = coin_groups['ruler']

for i in coin_groups.index:
	# this updates revised_ruler based on the ruler_conversion dictionary. This is for display (not data extraction)
	if coin_groups.ix[i,'ruler'] in ruler_conversion:
		coin_groups.set_value(i, 'revised_ruler', ruler_conversion[coin_groups.ix[i,'ruler']])

	# this section fills in the dates based on ruler (or denomination) if they are missing
	if (coin_groups.ix[i, 'revised_start'] != coin_groups.ix[i, 'revised_start']):
		temp_start = -1
		if coin_groups.ix[i, 'ruler'] != 'Unspecified ruler (contemporary copy)':
			try:
				temp_start = ruler_list[coin_groups.ix[i, 'ruler']][0]
			except:
				if coin_groups.ix[i, 'ruler'] not in ruler_conversion:
					print("Error: Unknown ruler: {}".format(coin_groups.ix[i, 'ruler']))				
		elif coin_groups.ix[i, 'ruler'] == 'Unspecified ruler (contemporary copy)':
			temp_start = year_limit(denomination_dates, coin_groups.ix[i, 'denomination'], "start")
		if temp_start != -1: coin_groups.set_value(i, 'revised_start', temp_start)

	if (coin_groups.ix[i, 'revised_end'] != coin_groups.ix[i, 'revised_end']):
		temp_end = -1
		if coin_groups.ix[i, 'ruler'] != 'Unspecified ruler (contemporary copy)':
			try:
				temp_end = ruler_list[coin_groups.ix[i, 'ruler']][1]
			except:
				if coin_groups.ix[i, 'ruler'] not in ruler_conversion:
					print("Error: Unknown ruler: {}".format(coin_groups.ix[i, 'ruler']))
		elif coin_groups.ix[i, 'ruler'] == 'Unspecified ruler (contemporary copy)':
			temp_end = year_limit(denomination_dates, coin_groups.ix[i, 'denomination'], "end")
		if temp_end != -1: coin_groups.set_value(i, 'revised_end', temp_end)


	# this section standardizes the mint names to those in FLAME's database
	try:
		if coin_groups.ix[i, 'mint'] == coin_groups.ix[i, 'mint']:
			try:
				coin_groups = coin_groups.set_value(i, 'mint', mint_conversion[coin_groups.ix[i, 'mint']])
			except:
				print("Error: Unknown mint: {}".format(coin_groups.ix[i, 'mint']))	# this should print nothing if working as intended
	except:
		continue

	# this section standardizes the denomination names to those in the FLAME database
	try:
		if coin_groups.ix[i, 'denomination'] == coin_groups.ix[i, 'denomination']:
			try:
				coin_groups = coin_groups.set_value(i, 'denomination', denomination_conversion[coin_groups.ix[i, 'denomination']])
			except:
				print("Error: Unknown denomination: {}".format(coin_groups.ix[i, 'denomination']))
	except:
		continue
	

#coin groups - to do:
# 	create update function to update only those entries that have been updated (as in the column)

# saving to files
coin_groups.to_csv('coin_groups.csv')
coin_finds.to_csv('coin_finds.csv')

#testing_database_connections()