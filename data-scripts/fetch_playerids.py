import os
import json

output = []
temp = []

#Goes through all the files in the gamelogs directory
for file in os.listdir('../data-local/gamelogs'):

	#Reads the json file and stores it
	try:
		with open('../data-local/gamelogs/'+file) as json_file:    
			data = json.load(json_file)
	except Exception, e:
		print('done')

	#Saves the name and id into an array
	temp = [file[0:-5],data['player_name']]
	output.append(temp)

#Saves as json file
with open('../data-local/player_ids.json', 'w') as outfile:
	json.dump(output, outfile)