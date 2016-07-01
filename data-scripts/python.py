# Executes all of the python scripts

# USAGE: python python [years] [season-type]

# EXAMPLE: (list of players)
# python fetch-agg-playerstats.py 2015-16 'Regular Season' '203092,203112'

# EXAMPLE: (all players)
# python fetch-agg-playerstats.py 2015-16 'Regular Season' 
import fetch_activeplayers
import fetch_agg_playerstats
import fetch_playerimages
import fetch_playersalary
import format_agg_playerstats
import requests
import sys

start = '20'+sys.argv[1][2:4]
end = '20'+sys.argv[1][5:]
while(start < end):
	season = str(int(end)-1)+'-'+end[2:]
	fetch_activeplayers.main(season)
	if sys.argv[2] == 'Regular Season':
		fetch_agg_playerstats.main(season,sys.argv[2])
	elif sys.argv[2] == 'Playoffs':	
		fetch_agg_playerstats.main(season,sys.argv[2])
	elif sys.argv[2] == 'Both':
		fetch_agg_playerstats.main(season,'Regular Season')
		fetch_agg_playerstats.main(season,'Playoffs')
	fetch_playerimages.main(season)
	fetch_playersalary.main(end)
	format_agg_playerstats.main(season)
	end=int(end)-1