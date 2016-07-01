#!/bin/sh
startY=0
endY=0
echo -n "Enter Start Year > "
read startY
echo -n "Enter End Year > "
read endY
#echo $startY + $endY
until [$endY == 1]; do
	echo python ./data-scripts/fetch-activeplayers.py $endY + '-' # + "${str: -2}"
	endY=`expr $endY - 1`
done