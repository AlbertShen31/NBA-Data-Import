# USAGE:
# python fetch_gamelogs.py [season] [player name (underscore separated)] 

# EXAMPLE python fetch_gamelogs.py 2015-16 steph_curry


import sys
import json
import urllib2
from bs4 import BeautifulSoup
import re


endyr = sys.argv[1][5:]
#Detects for multiple years
while (int(sys.argv[1][2:4]) < int(endyr)):
	season = '20'+str(int(endyr)-1)+'-'+str(endyr)
	#print(season)
	with open('../data-local/activeplayers/activeplayers_' + season + '.json') as activeplayers_file:
		activeplayers = json.load(activeplayers_file)

	start = False
	if (len(sys.argv) > 2):
		start=False
		name = sys.argv[2]
	else:
		start=True
		name = ''

	# loop through the activeplayers file, take the team info and add team/other info for each player obj
	for player in activeplayers['resultSets'][0]['rowSet']:

		playName = player[2].lower()
		playerID = player[0]

		if(playName[-3:] == 'jr.'):
			playName = playName[:-4]
		
		playName = re.sub('[!@#$-.]', '', playName)

		if(start or playName == (name.split('_')[0] + ' ' +  name.split('_')[1]) ):
			start = True
			if(playName == 'nene'):
				playName = 'nene hilario'
			elif(playName == 'jose juan barea'):
				playName = 'josejuan barea'
			elif(playName == 'luc mbah a moute'):
				playName = 'luc mbahamoute'
			elif(playName == 'james michael mcadoo'):
				playName = 'jamesmichael mcadoo'
			
			playername = playName.split(' ')[1][0:5] + playName.split(' ')[0][0:2] + "01"
			
			if(playName == 'jeff ayres'):
				playername = 'pendeje02'
			elif(playName == 'harrison barnes'):
				playername = 'barneha02'
			elif(playName== 'matt barnes'):
				playername = 'barnema02'
			elif(playName == 'bojan bogdanovic'):
				playername = 'bogdabo02'
			elif(playName == 'anthony brown'):
				playername = 'brownan02'
			elif(playName == 'markel brown'):
				playername = 'brownma02'
			elif(playName == 'clint capela'):
				playername = 'capelca01'
			elif(playName == 'anthony davis'):
				playername = 'davisan02'
			elif(playName == 'mike dunleavy'):
				playername = 'dunlemi02'
			elif(playName == 'danny green'):
				playername = 'greenda02'
			elif(playName == 'jeff green'):
				playername = 'greenje02'
			elif(playName == 'pj hairston'):
				playername = 'hairspj02'
			elif(playName == 'jordan hamilton'):
				playername = 'hamiljo02'
			elif(playName == 'tim hardaway'):
				playername = 'hardati02'
			elif(playName == 'tobias harris'):
				playername = 'harrito02'
			elif(playName == 'gerald henderson'):
				playername = 'hendege02'
			elif(playName == 'john holland'):
				playername = 'hollajo02'
			elif(player[6] == 'christapher_johnson'):
				playername = 'johnsch04'
			elif(playName == 'joe johnson'):
				playername = 'johnsjo02'
			elif(playName == 'stanley johnson'):
				playername = 'johnsst04'
			elif(playName == 'dahntay jones'):
				playername = 'jonesda02'
			elif(playName == 'james jones'):
				playername = 'jonesja02'
			elif(playName == 'brandon knight'):
				playername = 'knighbr03'
			elif(playName == 'david lee'):
				playername = 'leeda02'
			elif(playName == 'kevin martin'):
				playername = 'martike02'
			elif(playName == 'wesley matthews'):
				playername = 'matthwe02'
			elif(playName == 'andre miller'):
				playername = 'millean02'
			elif(playName == 'markieff morris'):
				playername = 'morrima02'
			elif(playName == 'marcus morris'):
				playername = 'morrima03'
			elif(playName == 'xavier munford'):
				playername = 'munfoxa02'
			elif(playName == 'larry nance'):
				playername = 'nancela02'
			elif(playName == 'willie reed'):
				playername = 'reedwi02'
			elif(playName == 'andre roberson'):
				playername = 'roberan03'
			elif(playName == 'glenn robinson'):
				playername = 'robingl02'
			elif(playName == 'jakarr sampson'):
				playername = 'sampsja02'
			elif(playName == 'jonathon simmons'):
				playername = 'simmojo02'
			elif(playName == 'greg smith'):
				playername = 'smithgr02'
			elif(playName == 'jason smith'):
				playername = 'smithja02'
			elif(playName == 'josh smith'):
				playername = 'smithjo03'
			elif(playName == 'isaiah thomas'):
				playername = 'thomais02'
			elif(playName == 'jason thompson'):
				playername = 'thompja02'
			elif(playName == 'kemba walker'):
				playername = 'walkeke02'
			elif(playName == 'alan williams'):
				playername = 'willial03'
			elif(playName == 'lou williams'):
				playername = 'willilo02'
			elif(playName == 'marcus williams'):
				playername = 'willima04'
			elif(playName == 'marvin williams'):
				playername = 'willima02'
			elif(playName == 'mo williams'):
				playername = 'willima01'
			elif(playName == 'metta world peace'):
				playername = 'artesro01'
			elif(playName == 'brandan wright'):
				playername = 'wrighbr03'
			
			# parse arguments
			displayname = playName.split(' ')[0].title() + " " + playName.split(' ')[1].title()
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
			with open('../data-local/gamelogs/' + str(playerID) + '.json', 'w') as outfile:
				json.dump(output, outfile)


	endyr =int(endyr)-1