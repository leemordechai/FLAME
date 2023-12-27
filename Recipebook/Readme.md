## Supply your own data for FLAME's recipe book
To supply your own data for FLAME's recipe book, it is best to use the suggested template (here). Adding more columns is not a problem, although they would not be analyzed in the current state of things. Note that each field requires a different type of input (e.g. text, numbers, TRUE/FALSE). Not all the columns that do exist are critical for the code in the cookbook to run, and we list a general priority below. 

A few words on the organization of the data. FLAME and its tools work through two main types of data: Coin Finds, which correspond to coins found at a specific site and a specific context (e.g. an excavation, a hoard, a single find) and Coin Groups, which correspond to a group of coins within the find that share a series of important features. In FLAME these important features include the dates of the coin, its metal and denomination, and its mint. The different sheets in the Excel file are connected based on the relevant ID numbers. These allow the code to create a whole connected ("relational") database out of these few separate tables.

1. ####CoinFindings sheet
* ID - the ID number of the find. This should be an arbitrary and unique number (integer), and is responsible for the key connection between the CoinFindings sheet and the coin_groups sheet. Necessary for the code to run. 
* cf_name - the name of the find; free text. This is important to identify the find. 
* cf_place_name - a Pleiades ID (if relevant). Can be left blank.
* cf_custom_place_name - the name of the place of the coind find. Should have some value. 
* cf_custom_x_coordinate, cf_custom_y_coordinate - the coordinates (longitude and langitude of where the coins were found). Necessary for any placement of the find on a map. Must be numbers with a decimal point.  
* cf_custom_region_vague - values are 0 (=certain or near certain location), 1 = (find comes from a place in a radius of <100km from the coordinates), 2 = (find comes from the region, i.e. >100km from the coordinates). Default should be 0. 
* cf_excavation_name - the excavation name, if relevant to differentiate it from others. Not necessary. 
* cf_excavation - TRUE if the find refers to an excavation, FALSE if not.
* cf_excavation_start - if an excavation, when did it begin. A 4-digit number (e.g. 1920), not necessary.
* cf_excavation_end - if an excavation, when did it end. A 4-digit number (e.g. 1920), not necessary.
* cf_single_find - TRUE if the find refers to a single find, FALSE if not.
* cf_hoard - TRUE if the find refers to a hoard, FALSE if not. Hoards found in excavations would have TRUE here and in the field "cf_excavation". 
* cf_start_year - the earliest year of coins represented in the find. Use negative for BCE years. Should be an integer. Not necessary. 
* cf_end_year - the latest year of coins represented in the find.  Use negative for BCE years. Should be an integer. Not necessary. 
* cf_vague - TRUE if the dates on the coins are vague, FALSE if they aren't. 
* cf_num_coins_found - the total number of coins found in the find, including coins that are not part of your dataset. Should be an integer. 
* cf_id_relevant_coins - if only some of the coins in the find are relevant, this field should include their IDs. 
* cf_publication_ref - the references for the find. Will be displayed to users. Not necessary.
* cf_user - the name of the user who entered the information. Not necessary. 
* cf_comment - comments to be displayed to users. Not necessary. 
* cf_date_entered - the date in which the coins were entered (format is 12/31/2020). Not necessary. 
* Region - Obsolete. 
* Tag_ID - Irrelevant. 
* Dataset_IDs - Irrelevant.

2. ####coin_groups
* cgID - the coin group ID. An arbitrary and unique number (integer). Necessary.
* cg_num_coins - the number of coins in the coin group, i.e. share the key characteristics below.
* cg_mintner - irrelevant. 
* cg_unknown_mint_area - TRUE if the location in which the coins were minted is unknown or vague; FALSE if not. 
* cg_start_year - the earliest year in which the coins in the coin group could have been produced. Integers only. Important for any analysis of coins. 
* cg_end_year - the latest year in which the coins in the coin group could have been produced. Integers only. Important for any analysis of coins. 
* cg_vague_time - FALSE if we know the dates of the two fields above with certainty, TRUE if they are otherwise vague. 
* cg_user - the name of the user who inputted this coin group. Not necessary. 
* cg_comment - any comments on the coin group. Not necessary.
* cg_custom_start_century - Irrelevant.
* cg_custom_end_century - Irrelevant.
* cg_imitation_start_year - Irrelevant.
* cg_imitation_end_year - Irrelevant.
* cg_imitation_ruler - Irrelevant.
* cg_imitation_dynasty - Irrelevant.
* Denomination_ID - ID of the denomination (see Denominations sheet). Necessary for any kind of filters using coin denominations.
* CoinFinding_ID - ID of the coin find (see CoinFindings sheet). Necessary to connect the data. 
* Ruler_ID - irrelevant.
* Dynasty_ID - ID of the dynasty (see Dynasties sheet). Not important. 
* Mint_ID - ID of the mint (see Mints sheet). Necessary to display any connections to mints on the map. 
* DateEntered - the date in which the coins were entered (format is 12/31/2020). Not necessary. 
* CustomStartPeriodID - irrelevant. 
* CustomEndPeriodID - irrelevant.
* IsMinter - irrelevant.
* Imported - irrelevant.

3. ####Metals
* ID - the metal ID. An arbitrary and unique number (integer). Necessary.
* MetalName - the name of the metal (e.g. gold).

4. ####Denominations
* ID - the denomination ID. An arbitrary and unique number (integer). Necessary.
* DenominationName - the name of the denomination
* Metal_ID - the corresponding metal ID from the Metals sheet

5. ####Dynasties
* ID - the dynasty's (or other political group name) ID. An arbitrary and unique number (integer). Necessary.
* DynastyName - the name of the dynasty (or other political group name), e.g. Romans.


