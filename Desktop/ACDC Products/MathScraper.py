## Wikipedia Scraper 1.0.0
## Written by David Freiberg
## Last updated December 12th, 2015

## Global Variables:

##	headers: The user agent to be sent to Wikipedia during scraping.  Not yet implemented.
##	path: The path all output files are written too.  By default, it is set to the directory this file is in.
##	URLPrefix: The API information before the query.  Sets the format to extract summaries and sets the articles per query to 20.
##	URLSuffix: The API information after the query.  Sets the format to JSON.

##	pages: A list of page titles and their associated categories.  The category information is currently unused.
##	titles: A list of page titles, taken from pages.

##	titlesFile: The output stream for the titles of each article, separated by "\n".
##	summariesFile: The output stream for the summaries of each article, separated by "\n--&&--\n".
##	exceptionsFile: The output stream for the exceptions generated while downloading, separated by "\n".

## Local Variables:

##	lowerIndex: The lower index of the slice of titles being queried.
##	upperIndex: The upper index of the slice of titles being queried.

##	JSONSummaries: The JSON obtained by the query, in raw form.
##	parsedJSONSummaries: The JSON obtained by the query, in multi-level dictionary form.
##		{...,
##		"query":
##			{...,
##			"pages":
##				{"__PAGEID1__":
##					{"pageid":__PAGEID1__,
##					...,
##					"title":__TITLE1__,
##					"extract":__SUMMARY1__},
##				{"__PAGEID2__":...},
##				...
##				}
##			}
##		}
##	query: The query for the Wikipedia scraper.  Consists of the article titles concatenated with "|" and with " " replaced by "_".
##	tempSummary: The summary, taken from parsedJSONSummaries if available, or blank if not available.
##	tempTitle: The title, taken from parsedJSONSummaries if available, or blank if not available.

import urllib
import time
import math
import codecs
import json
import os

headers = {"User-Agent" : "MRS Hackathon MaterialsScience Bot v3 (dnf28@drexel.edu)"}
URLPrefix = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=10&explaintext&exlimit=20&exintro&titles="
URLSuffix = "&format=json"

path =  os.path.dirname(os.path.abspath("MathScraper.py")) + "/"

## This creates a list of lists of the pages to be downloaded and their associated categories, and strips formatting.
## The PagesAndCategories file is assumed to be in the format '{"TITLE", "CATEGORY"}'.  This parser is untested for other formats.

pages = codecs.open(path + "ListOfMathPagesAndCategories.txt",encoding='utf-8').read()
pages = pages.split("\n")
pages = map(lambda x: x.strip("{\"}"),pages)
pages = map(lambda x: x.split("\", \""),pages)

titles = list(set(map(lambda x: x[0],pages)))

titlesFile = open(path + "mathTitles.txt",'a')
summariesFile = open(path + "mathSummaries.txt",'a')
exceptionsFile = open(path + "mathExceptions.txt",'a')

for i in range(0,int(math.ceil(len(titles)/20)) + 1):
	lowerIndex = 20*i
	upperIndex = min(20*(i+1)-1,len(titles))

	query = "|".join(map(lambda x: x.replace(" ","_"),titles[lowerIndex:upperIndex]))
	JSONSummaries = urllib.urlopen(URLPrefix + query.encode('utf-8') + URLSuffix).read()
	parsedJSONSummaries = json.loads(JSONSummaries)
	for pageID in parsedJSONSummaries["query"]["pages"]:
		try:
			tempTitle = parsedJSONSummaries["query"]["pages"][pageID]["title"]
			tempSummary = parsedJSONSummaries["query"]["pages"][pageID]["extract"]
		except KeyError as e:
			print "Exception "+str(e)+" caught between " +str(lowerIndex)+ " and " +str(upperIndex)+ " at pageID + " +pageID+"."
			exceptionsFile.write(pageID.encode('utf-8') + "\n")
			tempTitle = " "
			tempSummary = " "
		except:
			print "Exception caught between " + str(lowerIndex) + " and " + str(upperIndex) + "."
			exceptionsFile.write(pageID.encode('utf-8') + "\n")
			tempTitle = " "
			tempSummary = " "

		titlesFile.write(tempTitle.encode('utf-8') + "\n")
		summariesFile.write(tempSummary.encode('utf-8') + "\n --&&-- \n")

		print tempSummary
		print " "
	
	print upperIndex
	print " "
	time.sleep(3)
