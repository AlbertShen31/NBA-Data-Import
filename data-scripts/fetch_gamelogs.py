# USAGE:
# python fetch_gamelogs.py [player name (underscore separated)] 

# EXAMPLE python fetch_gamelogs.py 2015-16 steph_curry


import sys
import json
import urllib2
from bs4 import BeautifulSoup
import re
import os.path


##### function for resolving names #####
def matchNames(player_name):

	playername = player_name.split(' ')[1][0:5] + player_name.split(' ')[0][0:2] + "01"
	
	if(player_name == 'jeff ayres'):
		playername = 'pendeje02'
	elif(player_name == 'harrison barnes'):
		playername = 'barneha02'
	elif(player_name== 'matt barnes'):
		playername = 'barnema02'
	elif(player_name == 'bojan bogdanovic'):
		playername = 'bogdabo02'
	elif(player_name == 'anthony brown'):
		playername = 'brownan02'
	elif(player_name == 'markel brown'):
		playername = 'brownma02'
	elif(player_name == 'clint capela'):
		playername = 'capelca01'
	elif(player_name == 'anthony davis'):
		playername = 'davisan02'
	elif(player_name == 'mike dunleavy'):
		playername = 'dunlemi02'
	elif(player_name == 'danny green'):
		playername = 'greenda02'
	elif(player_name == 'jeff green'):
		playername = 'greenje02'
	elif(player_name == 'pj hairston'):
		playername = 'hairspj02'
	elif(player_name == 'jordan hamilton'):
		playername = 'hamiljo02'
	elif(player_name == 'tim hardaway'):
		playername = 'hardati02'
	elif(player_name == 'tobias harris'):
		playername = 'harrito02'
	elif(player_name == 'gerald henderson'):
		playername = 'hendege02'
	elif(player_name == 'john holland'):
		playername = 'hollajo02'
	elif(player[6] == 'christapher_johnson'):
		playername = 'johnsch04'
	elif(player_name == 'joe johnson'):
		playername = 'johnsjo02'
	elif(player_name == 'stanley johnson'):
		playername = 'johnsst04'
	elif(player_name == 'dahntay jones'):
		playername = 'jonesda02'
	elif(player_name == 'james jones'):
		playername = 'jonesja02'
	elif(player_name == 'brandon knight'):
		playername = 'knighbr03'
	elif(player_name == 'david lee'):
		playername = 'leeda02'
	elif(player_name == 'kevin martin'):
		playername = 'martike02'
	elif(player_name == 'wesley matthews'):
		playername = 'matthwe02'
	elif(player_name == 'andre miller'):
		playername = 'millean02'
	elif(player_name == 'markieff morris'):
		playername = 'morrima02'
	elif(player_name == 'marcus morris'):
		playername = 'morrima03'
	elif(player_name == 'xavier munford'):
		playername = 'munfoxa02'
	elif(player_name == 'larry nance'):
		playername = 'nancela02'
	elif(player_name == 'willie reed'):
		playername = 'reedwi02'
	elif(player_name == 'andre roberson'):
		playername = 'roberan03'
	elif(player_name == 'glenn robinson'):
		playername = 'robingl02'
	elif(player_name == 'jakarr sampson'):
		playername = 'sampsja02'
	elif(player_name == 'jonathon simmons'):
		playername = 'simmojo02'
	elif(player_name == 'greg smith'):
		playername = 'smithgr02'
	elif(player_name == 'jason smith'):
		playername = 'smithja02'
	elif(player_name == 'josh smith'):
		playername = 'smithjo03'
	elif(player_name == 'isaiah thomas'):
		playername = 'thomais02'
	elif(player_name == 'jason thompson'):
		playername = 'thompja02'
	elif(player_name == 'kemba walker'):
		playername = 'walkeke02'
	elif(player_name == 'alan williams'):
		playername = 'willial03'
	elif(player_name == 'lou williams'):
		playername = 'willilo02'
	elif(player_name == 'marcus williams'):
		playername = 'willima04'
	elif(player_name == 'marvin williams'):
		playername = 'willima02'
	elif(player_name == 'mo williams'):
		playername = 'willima01'
	elif(player_name == 'metta world peace'):
		playername = 'artesro01'
	elif(player_name == 'brandan wright'):
		playername = 'wrighbr03'

	return playername;

##### end matchNames() function #####


##### function to format name #####
def formatName(name):

	player_name = None;

	# remove "jr" from any player names
	if(name[-3:] == 'jr.'):
		player_name = name[:-4]

	# remove special chars from player names
	player_name = re.sub('[!@#$-.]', '', name)

	return player_name

##### end formatName() function


# user provided arguments
endyr = sys.argv[1][5:]

if(len(sys.argv) == 3):
	name = sys.argv[2]
else:
	name = None



# loop through each year specified in the range
while (int(sys.argv[1][2:4]) < int(endyr)):

	season = '20'+str(int(endyr)-1)+'-'+str(endyr)

	# get activeplayers list from the activeplayers_file (stored locally)
	with open('../data-local/activeplayers/activeplayers_' + season + '.json') as activeplayers_file:
		activeplayers = json.load(activeplayers_file)


	# loop through all players in the activeplayers file
	for player in activeplayers['resultSets'][0]['rowSet']:


		player_id = player[0]
		player_name = player[2].lower()


		# check if file already exists in filesystem for this player
		if not os.path.isfile("../data-local/gamelogs/" + str(player_id) + ".json"):

			player_name = formatName(player_name)

			# hard coded player name cases
			if(player_name == 'nene'):
				player_name = 'nene hilario'
			elif(player_name == 'jose juan barea'):
				player_name = 'josejuan barea'
			elif(player_name == 'luc mbah a moute'):
				player_name = 'luc mbahamoute'
			elif(player_name == 'james michael mcadoo'):
				player_name = 'jamesmichael mcadoo'
			
			playername = matchNames(player_name)
			

			# parse arguments
			displayname = player_name.split(' ')[0].title() + " " + player_name.split(' ')[1].title()
			season_endyr = '20'+str(endyr)

			print("PLAYERNAME: " + playername + "\n")
			print("SEASONENDYR: " + season_endyr + "\n")

			# (1) construct request url
			request_url = "http://www.basketball-reference.com/players/" + playername[0] + "/" + playername + "/gamelog/" + season_endyr + "/";
			print("downloading... " + request_url)

			# (2) download page as HTML file
			response = urllib2.urlopen(request_url)
			content = response.read()

			# (3) extract table from HTML document 
			content = BeautifulSoup(content)
			table = content.find("table", {"class":"sortable row_summable stats_table"})
			rows = table.find_all("tr");


			# (4) iterate over rows and get cell values
			print("length: " + str(len(rows)) + "\n")

			output = {}
			output['player_name'] = displayname
			output['player_id'] = None
			output[sys.argv[1]] = []

			for row in rows:

				# get cells in the row
				cells = row.find_all("td")
				game_arr = []

				if(cells and len(cells) > 9):
					for i in range(0,30):
						cellvalue = cells[i].get_text()
						game_arr.append(cellvalue)

				elif(cells and len(cells) == 9):
					for i in range(0,9):
						cellvalue = cells[i].get_text()
						game_arr.append(cellvalue)

				output[sys.argv[1]].append(game_arr)

			# write output to a json file
			with open('../data-local/gamelogs/' + str(player_id) + '.json', 'w') as outfile:
				json.dump(output, outfile)

		else:
			print("FILE ALREADY EXISTS FOR " + str(player_id) + ", SKIPPING")


	endyr-=1




