# Downloads player salaries for a given season

# USAGE:
# python fetch-playersalary.py [endyear]

# EXAMPLE:
# python fetch-playersalary.py 2013

import sys
import json
import csv
import time
import os.path
import urllib2
from bs4 import BeautifulSoup



endyear = sys.argv[1]
season = str(int(endyear)-1) + "-" + str(int(endyear) % 100)


# user agent header -- set to mozilla firefox browser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# current page number in the table
pagenum = 1

# for all pages in the table: 


# (1) construc URL to download
# request URL format:
# "http://espn.go.com/nba/salaries/_/year/[year]/page/2/seasontype/3"
request_url = "http://espn.go.com/nba/salaries/_/year/" + endyear + "/page/" + str(pagenum) + "/seasontype/3"
print("downloading... " + request_url)


# (2) download page as HTML file
response = urllib2.urlopen(request_url)
content = response.read()


# (3) extract table from HTML document 
content = BeautifulSoup(content)
table = content.find("table", {"class":"tablehead"})

rows = table.find_all("tr");




# (4) iterate over rows and get cell values
output = ""
for row in rows:

	# get cells in the row
	cells = row.find_all("td")

	# iterate through all of the cells in the row
	for i in range(0,4):
		if(i == 1):

			name = cells[i].get_text()
			name = name.split(',')[0]
			output += (name + ", ")
		elif(i == 3):
			output += (cells[i].get_text().replace(',', '') + "\n")




# (5) output stirng to a csv file
print(output)

csvfile = open('../data-local/salaries/salaries_' + season + '.csv', 'w')
csvfile.write(output)



















