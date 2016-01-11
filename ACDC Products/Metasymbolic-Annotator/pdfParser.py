# Title: pdfParser
#
# Purpose: Intelligent Automatic Materials Science
#          Technical Paper Term Interpreter  Different Levels of Reader Comprehension using Hierarchical
#          Data Structures
#
# Author: Axel-Jose Persinger
#
# Co-Author: Christine Palmer  htmlUI() method | David Freiberg  hierarchy algorithm


# Imports a PDF parsing package
import textract
# Imports a webbrowser creating package
import webbrowser




#----------------  JSON or SQL Scraper here  ----------------#
#------------------------------------------------------------#




#----------------  Global Variables ----------------#
# 'append' opens a file  writing that will keep the words of all the positively matched terms
# 'defined' opens a file  writing that will keept the summaries of all the positively matched terms
# 'summary' opens the entire dictionary of summaries
# 'title' opens the entire dictionary of words
append = []
defined = []
summary = open('HierarchySummaries.txt').read()
summary = summary.split("--&&--")
title = open('hierarchyIndex.txt').read()
title = title.split("\n")
   # Creates lists to store words
dict0 = []
dict1 = []
dict2 = []
dict3 = []
dict4 = []

#---------------------------------------------------#




#----------------  Gets the source pdf and difficulty ----------------#
# Gets user input and returns the difficulty and the pdf text
def source():
    # Create a list 'text' to store the words of source.pdf
    # text = textract.process(input("Enter File path (Enter path in double quotes): "))
    text = textract.process("source.pdf")
    text = text.split()

    # Gets user's difficulty rating
    # difficulty = input("Please enter difficulty rating (0 being most explanatory, 4 being least): ")
    difficulty = 2
    difficulty = int(difficulty)

    return (text, difficulty)
#---------------------------------------------------------------------#




#----------------  Make sure that twoSentences.py has run at this point  ----------------#
# Modifies the summary text file so each definition is only two sentences long
def twoSentences():
    # Creates two indices that will cover over two sentences
    indexFirst = 0
    indexSecond = 0

    # Checks to make sure the two periods aren't in "etc." "i.e."
    rightSide = ['e', 'g', 't', 'c']
    leftSide = ['i', 'e', 't', 'c']

    for definition in summary:
        indexFirst = definition.find(".")
        indexSecond = definition.find(".", indexFirst + 1)

        # If there is only one period (theree one sentence) leave as is
        if (indexSecond - 1) == -1:
            definition = definition
        elif indexSecond == -1:
            definition = definition
        elif (((definition[indexSecond - 1]) not in leftSide) and ((definition[indexSecond + 1]) not in rightSide)):
            definition = (definition[:indexSecond + 1])
#-------------------------------------------------------------------------------------------#



#----------------  Make sure that 0...n.txt are created  ----------------#
# Creates lists that sorts the word based on difficulty
def hierarchymatter():

    # Opens file that keeps all hierarchy indices
    hNumbers = open('hierarchyNumbers.txt').read()
    hNumbers = hNumbers.split()

    k = 0

    # Goes through each word and storts
    for name in title:
        # DO NOT REMOVE THIS LINE OF CODE. IT WILL BREAK
        if k == len(hNumbers):
            break
        elif int(hNumbers[int(k)]) < 15:
            dict4.append(title[k] + "\n")
        elif int(hNumbers[int(k)]) >= 15 and int(hNumbers[int(k)]) < 40:
            dict3.append(title[k] + "\n")
        elif int(hNumbers[int(k)]) >= 40 and int(hNumbers[int(k)]) < 100:
            dict2.append(title[k] + "\n")
        elif int(hNumbers[int(k)]) >= 100 and int(hNumbers[int(k)]) < 300:
            dict1.append(title[k] + "\n")
        elif hNumbers[k] > 300:
            dict0.append(title[k] + "\n")
        k += 1

#------------------------------------------------------------------------#




#----------------  Parses through PDF and saves a file  the words and definitions that were crossed referenced  ----------------#
# Cross references all words in the dictionary to that in the PDF
def parser():
    #Gets text and difficulty from source method
    text, difficulty = source()

    # 'titleList' is a list object that keeps all the positively found terms bee transferring them over to append
    titleList = []


    # The  loop iterates through all the words in the pdf looking  positive terms matching per difficulty
    for word in text:
        if difficulty == 0:
             for titleWord in dict0:
                if titleWord == word:
                    titleList.append(titleWord)

        if difficulty == 1:
            for titleWord in dict1:
                if titleWord == word:
                    titleList.append(titleWord)

        if difficulty == 2:
            for titleWord in dict2:
                if titleWord == word:
                    titleList.append(titleWord)

        if difficulty == 3:
            for titleWord in dict3:
                if titleWord == word:
                    titleList.append(titleWord)

        if difficulty == 4:
            for titleWord in dict4:
                if titleWord == word:
                    titleList.append(titleWord)

	print titleList
	print difficulty
    return titleList
#----------------------------------------------------------------------------------------------------------------------------------#




#----------------  Remove duplicates from any given list  ----------------#
# Removes duplicates in the list titleList
def duplicateRemover(wordList):
    wordList = list(set(wordList))

    return wordList
#-------------------------------------------------------------------------#




#----------------  Writes any given list to a file  ----------------#
#Writes list fo file
def fileWriter (wordList):
    # Writes wordList to append and find subsequent summaries  it
     for item in wordList:
        append.append(str(item) + "\n")
        defined.append(summary[title.index(item)] + "\n")
#-------------------------------------------------------------------------#




#----------------  Loose run  ----------------#
print "Running: \n"
twoSentences()
hierarchymatter()
listWords = parser()
listWords = duplicateRemover(listWords)
fileWriter(listWords)
#----------------------------------------------#
print append
print defined



#----------------  Create HTML  ----------------#
# Creates basic HTML framework  the UI
def htmlUI():

    # Opens the dictionary files  reading
    titleHTML = append

    summaryHTML = defined


    # source variable keeps the source pdf
    url = "source.pdf"

    # Dictionary variable keeps the final dictionary to display
    dictionary = ""

    # Seperator variable seperates terms  aesthetics
    seperator = "\n--------\n"

    print len(titleHTML)
    print len(summaryHTML)

    i = 1
    for i in xrange(0,len(titleHTML) - 1):
        dictionary += titleHTML[i] + ":\n" + summaryHTML[i] + """<p>""" + seperator + """</p>"""
        i+=1

    print dictionary
    # Stores the HTML code
    htmlCode= """

    <div style="height:500px;width:300px;top:100;float:left;border:1px solid #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;">

    <div class="Table">
    <div style="font-size: 18pt; color: blue;">
        <p><b>AnnotatorXtreme</b><img src="http://archived.materials.drexel.edu/News/Logos/drexel-mse.png" alt="Drexel MSE Logo" border=3 height=80 width=250/></p>
    </div>
    <div class="Heading">

    """ + dictionary + """

    </div>

    </div>

    </div>
    <embed src=""" +url+ """ width="900" top="100" height="600" top="1" alt="pdf" pluginspage="http://www.adobe.com/products/acrobat/readstep2.html">
    """

    # Creates an HTML file to store everything and then closes it from memory
    Html_file= open("UI.html","w")
    Html_file.write(htmlCode)
    Html_file.close()

    # Opens the default browser to the HTML File
    webbrowser.open("UI.html")
#------------------------------------------------#



htmlUI()
