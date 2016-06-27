# USAGE: python fetch-activeplayers [season]
# EXAMPLE: python fetch-activeplayers 2015-16

# Fetches all active players for the given season

import requests
import sys
import json


if len(sys.argv) < 2:
	print "ERROR: must provide the current season as an argument"
	sys.exit(2)
else:
	request_url = "http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=1&LeagueID=00&"
	season = sys.argv[1]
	# print(request_url + "Season=" + season);

	# get me all active players for the specified season
	url_allPlayers = (request_url + "Season=" + season)
	 
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	#request url and parse the JSON
	response = requests.get(url_allPlayers, headers=headers)

	with open('../data-local/activeplayers/activeplayers_' + season + '.json', 'w') as outfile:
	    json.dump(response.json(), outfile)

