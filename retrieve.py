
import shutil
import sys
import os
import nltk
from string import punctuation
import urllib
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import itertools
import re
import math
import time

#######################################################################################################################
# The list of stopwords is read from the given location and punctuations are added to it.
# These two together form the custom stopwords
#######################################################################################################################

def buildCustomStopwords():
    url = "https://www.csee.umbc.edu/courses/graduate/676/term%20project/stoplist.txt"
    httpfile = urlopen(url).read()
    container = httpfile.decode("utf8")
    # print("punctuation : ",punctuation)
    punck=list(punctuation)
    StopWords = container + ','.join(punck)
    return StopWords

#######################################################################################################################
# The plain text obtained from cmd line is now cleaned by removing the stopwords,
# removing the words of length one and the ones that occur just once
#######################################################################################################################
def cleanText(textSoupList,stopWords):

    textSoupListString = " ".join(textSoupList)
    words = nltk.word_tokenize(textSoupListString)
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word for word in words if not re.search('^[0-9]+\\.[0-9]+$', word)]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in stopWords]
    return words


######################################################################################################################
#The query is taking as system arguemts apart from sys.argv[0] which is the scirpt name are the terms in the search query
########################################################################################################################
strOne = ""

count = 0
for x in sys.argv:
    if count != 0:
         strOne += ' '+x
         # print(strOne)
    count+=1

# userInput = input("Enter the sentence to search : \n")

# print("Entered sentence : ",strOne)
#######################################################################################################################
#The stopwords are removed from the typed in query , it is tokenized into single tokens and cleaned using the cleaning
#function above
#######################################################################################################################

word_tokens = nltk.word_tokenize(strOne)

# print("The word_tokens : ",word_tokens)

stopWords = buildCustomStopwords()
cleaned_words = cleanText(word_tokens,stopWords)

# print("The cleaned_words : ",cleaned_words)

#######################################################################################################################

#Each token or word from the query is searched for in the dictionary file created in assignment 3 , this file contains
#the term , the no of documents the term occurs in and the first position of this term in the postings file
#Once the term is obtained in the dictionary file , the next 2 lines conatining the frequency and postion is also
#saved in memeory as freq and pos
#Then we go to the postion mentioned in pos in the postings file. From this location we get the document id and term
#weights of that term in that document, this is done for the times of freq values.
#A dictionary is created final Dict which has the document id as keys and term and its weights as values.
#Here boolean OR is used to check similarity , we consider a document if it conatns one or many of the query terms as
# a success document.
#Hence term weights for every such success document is calculated
#######################################################################################################################
finalDict = {}

for each_word in cleaned_words:
    # print("Processing word : ", each_word)

    with open("C:\\Users\divya\Desktop\Output\dictionaryFile.txt") as openfile:


            for line in openfile:
                # print("line : ",line)
                # print("each_word : ", each_word)



                line = line.replace('\n','')
                line = line.strip()

                each_word = each_word.replace('\n','')
                each_word = each_word.strip()

                if each_word == line:

                    print("Foundword : ",line)
                    freq = str(next(openfile)).replace('\n','')
                    pos = int((next(openfile)).replace('\n',''))
                    pos = pos - 1

                    print("The freq : ",freq)
                    print("The pos : ", pos)



                    f = open("C:\\Users\divya\Desktop\Output\\postingsFile.txt")
                    lines = f.readlines()

                    for i in range(int(freq)):

                        dict_queryWords = {}

                        print("Getting records : ",lines[int(pos)+i])

                        docANDweight = lines[int(pos)+i]

                        # print(docANDweight.split(','))

                        strList = docANDweight.split(',')

                        # print(strList[0])
                        # print(strList[1])

                        doc_id = strList[0]
                        weight = strList[1].replace('\n','')



                        dict_queryWords.update({each_word: weight})
                        #print("Each word dictionary : ",dict_queryWords)
                        #print('For doc : ',doc_id)

                        if doc_id in finalDict.keys():
                            print("The doc is prenset : ",doc_id)
                            # print("Getting : ",finalDict[doc_id])
                            mergeDict = finalDict[doc_id]
                            # print("The existing word : ",mergeDict)
                            mergeDict.update(dict_queryWords)
                            # print("Updated mergeDict : ",mergeDict)
                            finalDict[doc_id] = mergeDict
                            #print("Final in if: ",finalDict)
                            # finalDict.update({doc_id:dict_queryWords})

                        else:
                            # print("The doc_id is not present : ",doc_id)
                            finalDict.update({doc_id:dict_queryWords})
                            #print("Updated in else : ",finalDict)

print("The final dictornay : ",finalDict)



#######################################################################################################################
#A dictionary is created final Dict which has the document id as keys and term and its weights as values.
#Here boolean OR is used to check similarity , we consider a document if it conatns one or many of the query terms as
# a success document.
#Hence term weights for every such success document is calculated
#######################################################################################################################



addThis = 0.0

finalDisplay = {}


for k1,v1 in finalDict.items():
    print("For doc : ",k1)
    addThis = 0.0
    for k2,v2 in v1.items():
            #print("For word : ",k2)
            #print('Add these : ',float(v2))
            addThis += float(v2)
            #print('Added : ',addThis)
            finalDisplay.update({k1:addThis})
            #print("AddingtoFinalDisplay: ", finalDisplay)


print("Here Also : ",finalDisplay)


#######################################################################################################################
#Success documents with term weights sum is added to a new dictionary
#Top 10 documents with higher values of terms weights is displayed as top 10 documents for the query search
#######################################################################################################################


counter = 0

a1_sorted_keys = sorted(finalDisplay, key=finalDisplay.get, reverse=True)
for r in a1_sorted_keys:
    print(str(r)  +'.html ' +  str(finalDisplay[r]))
    counter+=1
    if counter == 10:
        # print("finished top 10")
        break
