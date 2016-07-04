# USAGE:
# python fetch_gamelogs.py [player name (underscore separated)] [season]

# EXAMPLE python fetch_gamelogs.py steph_curry 2015-16


import sys
import json
import urllib2
from bs4 import BeautifulSoup


# parse arguments
playername = sys.argv[1].split('_')[1][0:5] + sys.argv[1].split('_')[0][0:2] + "01"
displayname = sys.argv[1].split('_')[0].title() + " " + sys.argv[1].split('_')[1].title()
season_endyr = sys.argv[2].split('-')[0][0:2] + sys.argv[2].split('-')[1]

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
output[sys.argv[2]] = []

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

	output[sys.argv[2]].append(game_arr)


# write output to a json file
with open('../data-local/gamelogs/' + playername + '.json', 'w') as outfile:
	json.dump(output, outfile)








