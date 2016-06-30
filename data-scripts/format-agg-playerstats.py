# input files are in ../data-local
# output file is in ../data-local/agg-playerstats/

# EXAMPLE:
# python format-agg-playerstats.py ../data-local/agg-playerstats_2015-16.json

import sys
import json
import csv
import re

# Name Conversion Helper Function #
def normalizeName(fullname):
	if(fullname == 'Patrick Mills'):
		return 'Patty Mills'
	elif(fullname == 'Joseph Young'):
		return 'Joe Young'
	elif(fullname == 'Nene Hilario'):
		return 'Nene'
	elif(fullname == 'Tim Hardaway'):
		return 'Tim Hardaway Jr.'
	elif(fullname == 'Chuck Hayes'):
		return 'Charles Hayes'
	elif(fullname == 'Jose Juan Barea'):
		return 'J.J. Barea'
	else:
		return fullname

# Remove players with incomplete stats data
def removeNullPlayers(players):
	for player in players:

		if not 'stats' in player or not 'per100stats' in player:
			print("----- DELETE PLAYER -----")
			print(player)
			players.remove(player)

	return players



# create output json object and initialize fields 
output = {}
season = None;
season_type = None;


# load agg-playerstats JSON file 
with open(sys.argv[1]) as agg_playerstats_file:
	agg_playerstats = json.load(agg_playerstats_file)

# set season and season_type values
season = agg_playerstats['season']
season_type_field = agg_playerstats['season-type']
if season_type_field == "Regular Season":
	season_type = 'r'
elif season_type_field == "Playoffs":
	season_type = 'p'


# change the dash in the "season-type" key to an underscore
output['season'] = agg_playerstats['season']
output['season_type'] = agg_playerstats['season-type']
output['data'] = []



# load activeplayers JSON file 
with open('../data-local/activeplayers/activeplayers_' + season + '.json') as activeplayers_file:
	activeplayers = json.load(activeplayers_file)

# loop through the activeplayers file, take the team info and add team/other info for each player obj
for player in agg_playerstats['data']:
	playerid = player['player_id'];
	new_playerobj = player;

	# find the current player in active player records 
	for playerprofile in activeplayers['resultSets'][0]['rowSet']:
		if playerprofile[0] == playerid:
			# append additional info from activeplayers record to  player obj
			new_playerobj['team'] = playerprofile[10]
			new_playerobj['startYear'] = playerprofile[4]
			new_playerobj['endYear'] = playerprofile[5]
			new_playerobj['hasPlayed'] = playerprofile[12]

	# print(new_playerobj)
	output['data'].append(new_playerobj)




# load nba advanced stats CSV file
advancedstats_file = open('../data-local/input/' + season + '/nba_' + season + '_advanced.csv')
as_reader = csv.reader(advancedstats_file)

# loop through the advanced stats CSV file and append advanced stats fields to player obj
for player in output['data']:

	# reset position of read position
	advancedstats_file.seek(0)
	
	prev_player = None;
	# find the current player in advanced stats records
	for row in as_reader:

		if(len(row) > 1):

			# convert names to lowercase and remove non-alphanumeric characters
			as_name = normalizeName(row[1])
			output_name = normalizeName(str(player['player_name']))

			as_name = ''.join(as_name.split()).lower()
			output_name = ''.join(output_name.split()).lower()

			as_name = re.sub(r'\W+', '', as_name)
			output_name = re.sub(r'\W+', '', output_name)

			if(as_name == output_name and prev_player != as_name):

				# print('found a match!' + row[1])
				player['position'] = row[2]
				prev_player = as_name

				as_list = row[7:19] + row[20:24] + row[25:29]
				player['advancedstats'] = []

				for val in as_list:
					if(val == ''):
						player['advancedstats'].append(None)
					else:
						player['advancedstats'].append(float(val))



# load nba per100 stats CSV file
per100stats_file = open('../data-local/input/' + season + '/nba_'  + season + '_per100.csv')
per100_reader = csv.reader(per100stats_file)

# loop through the per100 stats CSV file and append advanced stats fields to player obj
count = 0
for player in output['data']:

	# reset position of read position
	per100stats_file.seek(0)
	
	prev_player = None
	# find the current player in per100 stats records
	for row in per100_reader:

		if(len(row) > 1):
			# convert names to lowercase and remove non-alphanumeric characters
			as_name = normalizeName(row[1])
			output_name = normalizeName(str(player['player_name']))

			as_name = ''.join(as_name.split()).lower()
			output_name = ''.join(output_name.split()).lower()
			
			as_name = re.sub(r'\W+', '', as_name)
			output_name = re.sub(r'\W+', '', output_name)

			if(as_name == output_name and prev_player != as_name):
				prev_player = as_name
				count += 1

				per100_list = row[8:29] + row[30:32]

				player['per100stats'] = []
				for val in per100_list:
					if(val == ''):
						player['per100stats'].append(None)
					else:
						player['per100stats'].append(float(val))


# load player contracts CSV file
contracts_file = open('../data-local/input/' + season + '/nba_' + season + '_playercontracts.csv')
contracts_reader = csv.reader(contracts_file)


# loop through the contracts stats CSV file and append salary info to player obj
count = 0
for player in output['data']:

	# reset position of read position
	contracts_file.seek(0)
	
	prev_player = None
	print(str(player['player_name'])+' '+ str(count2))
	# find the current player in per100 stats records
	for row in contracts_reader:
		
		if(len(row) > 1):
			# convert names to lowercase and remove non-alphanumeric characters
			#print(as_name)
			
			as_name = normalizeName(row[0])
			output_name = normalizeName(str(player['player_name']))

			as_name = ''.join(as_name.split()).lower()
			output_name = ''.join(output_name.split()).lower()
			
			as_name = re.sub(r'\W+', '', as_name)
			output_name = re.sub(r'\W+', '', output_name)

			if(as_name == output_name and prev_player != as_name):
				prev_player = as_name
				count += 1
				player['salary'] = row[1]



# remove null players (players with no stats data)
output['data'] = removeNullPlayers(output['data'])

print("Created: " + str(count) + " player records")

# write output to a json file
with open('../data-local/agg-playerstats/formatted-agg-playerstats_' + season_type + season + '.json', 'w') as outfile:
	json.dump(output, outfile)











