To supply your own data for FLAME's recipe book, it is best to use the suggested template (here). Adding more columns is not a problem, although they would not be analyzed in the current state of things. Note that each field requires a different type of input (e.g. text, numbers, TRUE/FALSE). Not all the columns that do exist are critical for the code in the cookbook to run, and we list a general priority below. 

1. CoinFindings sheet
* ID - the ID number of the find. This should be an arbitrary number (integer), and is responsible for the key connection between the CoinFindings sheet and the coin_groups sheet. Necessary for the code to run. 
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

2. coin_groups


