# Downloads player images for a given season

# USAGE: python fetch-playerimages.py [season]

# EXAMPLE:
# python fetch-playerimages.py 2015-16


import requests
import sys
import json
import time
import urllib
import os.path

def main(season):


	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	if len(sys.argv) < 2:
		print "ERROR: must provide the current season and season type as arguments"
		sys.exit(2)

	else:
		request_url = "http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=1&LeagueID=00&"
		print(request_url + "Season=" + season);

		# get me all active players for the specified season
		url_allPlayers = (request_url + "Season=" + season) 		
		response = requests.get(url_allPlayers, headers=headers)
		response.raise_for_status()
		
		# get an array of ids for active players in the given season
		players = response.json()['resultSets'][0]['rowSet']
		ids = [players[i][0] for i in range(0, len(players))]
		print(ids);



		# download images for each player in ids
		for i in ids:

			small_outputpath = "../data-local/imgs-playerprofile/small/" + str(i) + ".png"
			large_outputpath = "../data-local/imgs-playerprofile/large/" + str(i) + ".png"

			# check if the files already exist
			if not os.path.isfile(small_outputpath) or not os.path.isfile(large_outputpath):

				# construct 132x132 image url
				smallimg_url = "http://stats.nba.com/media/players/132x132/" + str(i) + ".png"

				# construct 230x185 image url
				largeimg_url = "http://stats.nba.com/media/players/230x185/" + str(i) + ".png"

				print('\ndownloading... ' + smallimg_url + '\n');
				print('downloading... ' + largeimg_url + '\n');


				try:
					# save images to data-local directory
					urllib.urlretrieve(smallimg_url, small_outputpath)
					urllib.urlretrieve(largeimg_url, large_outputpath)
				except Exception as e:
					print e.__doc__
					print e.message

				# wait for 2 seconds before fetching the next player's images
				time.sleep(2)
				print('waiting for 2 seconds... ')

			else:
				print(small_outputpath + " already exists")
				print(large_outputpath + " already exists")









