# USAGE: python fetch-activeplayers [season]
# EXAMPLE: python fetch-activeplayers 2015-16

# Fetches all active players for the given season

import requests
import sys
import json

def main(season):

	if len(season) < 2:
		print "ERROR: must provide the current season as an argument"
		sys.exit(2)
	else:
		request_url = "http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&"
		#season = sys.argv[1]
		# print(request_url + "Season=" + season);

		# get me all active players for the specified season
		url_allPlayers = (request_url + "Season=" + season)
		 
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

		#request url and parse the JSON
		response = requests.get(url_allPlayers, headers=headers)

		jsonobj = response.json()

		beginyr = int(season[:4])
		endyr = beginyr + 1
		print("beginyr : " + str(beginyr))
		print("endyr : " + str(endyr))

		output = {}
		output['resource'] = "activeplayers"
		output['resultSets'] = []
		output['resultSets'].append({})
		output['resultSets'][0]['rowSet'] = []


		for player in jsonobj['resultSets'][0]['rowSet']:
			startseason = int(player[4])
			endseason = int(player[5])
			if(startseason <= beginyr and endseason >= endyr):
				output['resultSets'][0]['rowSet'].append(player)


		with open('../data-local/activeplayers/activeplayers_' + season + '.json', 'w') as outfile:
		    json.dump(output, outfile)

