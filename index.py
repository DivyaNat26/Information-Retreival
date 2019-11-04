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
# List out the files in the input directory and read each one of them separately. It returns the list of filenames
#######################################################################################################################
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


def readFromDirectory():
    # print("\nReading from Directory...")
    fileNameList = []
    for filename1 in os.listdir(inputPath):
        filename = inputPath + "\\" + filename1
        fileNameList.append(filename)
    # print("--> Total files processed : ",len(fileNameList))
    return fileNameList


#######################################################################################################################
# Every file from the list is passed into an html parser to get the plain text without any html tags
#######################################################################################################################


def htmlParser(eachFile):
    textSoupList = []
    INP = open(eachFile, encoding="utf8", errors='ignore')
    soup = BeautifulSoup(INP, 'html.parser')
    text_soup = soup.get_text()
    # print("text_soup : ",text_soup)
    textSoupList.append(text_soup)
    # print("--> Parsing of", len(textSoupList), "files complete")
    return textSoupList


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
# The plain text obtained from the html parser is now cleaned by removing the stopwords,
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



#######################################################################################################################
# A dictionary is formed of every (document name[k]: [v] , token[k]:[v] ,Frequency[k] : [v]
#######################################################################################################################



def freqdictionary(theWords):

    freqdicList=[]
    freq_dict={}

    # textSoupListString = " ".join(theWords)
    # words = nltk.word_tokenize(textSoupListString)

    # print ("words join : ",theWords)

    for word in theWords:
        if word in freq_dict:
            freq_dict[word]+=1
        else:
            freq_dict[word]=1
        temp={'id':i,'freq_dict':freq_dict}

    freqdicList.append(temp)

    return freqdicList


#######################################################################################################################
# Term Frequency of every token is calculated with respect to the particular document using the formula below
#  (Number of times term t appears in a document)/ (Total number of terms in the document)
#######################################################################################################################
def getTermFreq(freqdicList):

    counter=0
    theTF = []
    for eachDoc in freqdicList:

        # print("The each Doc : ",eachDoc)
        for k in eachDoc['freq_dict']:
            # print("The freqdist of the doc : ",i)

            temp={'id':i,'term':k, 'TF': eachDoc['freq_dict'][k]/theWordsLength}
            # print("The TF of the term : ",temp)
            theTF.append(temp)

    return theTF


def getWordPosition(counter,k):
    #print("####################################### Getting the first position : ",listOfFiles)

    filename = '{:03}'.format(int(counter))
    #print("The file name present in : ",filename)

    #print("THE WORDS!!! : ",docAndWords.get('id'))
    #print("Find : ",k)
    #print("Index : ",docAndWords.get(filename).index(k))
    return docAndWords.get(filename).index(k)







def getAllDocWordCount(allFreqDist):

    print("Getting all document word count")
    theWordCount = []
    counter = 0
    alllistWrite = []





    for eachfreqdicList in allFreqDist:
        counter += 1

        for k in eachfreqdicList['freq_dict'].keys():

            # print("#### PRocessing the word : ",k)
            WordDic = {}
            count = 0
            for firstList in allFreqDist:
                if (k in firstList['freq_dict']):
                    count += 1
                    if(count==1):
                        # print("Found for the first time")
                        # print("The document in which it occurs : ",counter)
                        position = getWordPosition(counter,k)
                        # print("The final position : ",position)

                WordDic['word'] = k
                WordDic[counter] = ''

                mainWordDic.append(WordDic)

            # listWrite = k + '\n' + str(count) + '\n' + str(position) + '\n'

            alllistWrite.append(k)
            alllistWrite.append(str(count))
            alllistWrite.append(str(position))


        # print("The mainWordDic : ",mainWordDic)
        # print("The final list : ",alllistWrite)

        writeOutput('\n'.join(alllistWrite), "output1")

        temp = {'term': k, 'count': count}
        # print("The term word count : ",temp)
        theWordCount.append(temp)

    return theWordCount



######################################################################################################################
# Inverse Document Frequency of every word is calculated and normalised taking into account the whole document length
# using the formula below.
# log_e(Total number of documents / Number of documents with term t in it)
#######################################################################################################################


def getIDF(allFreqDist):

    # total docs / number of docs it comes in

    print("\nGetting IDF")
    print("The total number of documents : ",numOfDocs)

    allIDF = []
    counter = 0


    # print("allfreqdicList : ",allfreqdicList)

    for eachfreqdicList in allFreqDist:
        # print("eachfreqdicList : ",eachfreqdicList)
        # print("The keys : ",eachfreqdicList['freq_dict'].keys())
        oneMore = []
        counter+=1
        for k in eachfreqdicList['freq_dict'].keys():
            count = 0
            for firstList in allFreqDist:
                if (k in firstList['freq_dict']):
                        count+=1

            temp = {'id': counter, 'term': k, 'IDF': math.log(numOfDocs/count)}
            #
            # listWrite = k + '\n' + str(count) + '\n' + str(count) + '\n'
            # writeOutput(listWrite,str(counter))

            # print("The IDF Temp : ",temp)
            oneMore.append(temp)
        allIDF.append(oneMore)

    # print("The total IDF : ",allIDF)
    return allIDF


#################################################################
# A final TF-IDF score is calculated by the product of TF and IDF
#################################################################



def calculateTFIDF(allTFs,allIDF):

    #print("\nCalculating TFIDF")
    allTFIDF = []
    listWrite= []

    idfCounter = 0

    # data = {'001': ['0.12941089463812197', '0.17273259342311856', '0.19439344281561685', '0.15107174403062026'],
    #         '002': ['0.19439344281561685', '0.07341841122474525', '0.1335837506576383', '0.10775004524562369']}
    #
    # df = pd.DataFrame(data, index=['testimony', 'statement', 'privacy', 'federal'])

    for x,y in zip(allTFs,allIDF):
        # print("x : ", x)
        # print("x id : ",x['id'])

        tdmIndexWords.append(x['term'])


        TFIDF = x['TF'] * y['IDF']

        # updateTDMMatrix(x['id'],TFIDF)

        writeStr = x['term'] + "," + str(TFIDF)
        listWrite.append(writeStr)


    # writeOutput("\n".join(listWrite),"output2")



    return TFIDF



#######################################################################################################################
# Output of every token in every document is written to the corresponding wts text file
# Therefore at the end of this function we have 503 files containing tokens and their TFIDF scores
#######################################################################################################################



def writeOutput(listWrite,filename):

    output = Output + "\\" + filename + ".txt";
    with open(output, "a", encoding="utf-8",errors='ignore') as f:
        f.write(listWrite)



def buildDF(words, xColNames = None, **kwargs):


    #print("words : ",words)


    vectorizer = TfidfVectorizer()
    x1 = vectorizer.fit_transform(words)

    # print('x1 : ',x1)

    #create dataFrame
    df = pd.DataFrame(x1.toarray().transpose(), index = vectorizer.get_feature_names())

    # print('x1.toarray().transpose() : ', x1.toarray().transpose())

    if xColNames is not None:
        df.columns = xColNames

    return df


# def clearOutput(path):
#
#     #print("Clearing output folder")
#
#     if os.path.isfile(path):
#         os.remove(path)
#         os.mkdir(path, 0o755)
#     elif os.path.isdir(path):
#         #print("Here1")
#         shutil.rmtree(path)
#         #print("Here1")
#         os.mkdir(path, 0o755)
#     else:
#         os.mkdir(path, 0o755)

def clearOutput(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))
    os.mkdir(path, 0o755)

#######################################################################################################################
# Input files' location are taken as Sys.argv[1] and output files location as sys.argv[2].
# A timer is started at the beginning of the preprocessing of the document and ends when all the tokens and the weights
# are written to respective output files
#######################################################################################################################



startTime = time.time()

listOfFiles = ""
inputPath = sys.argv[1]
Output = sys.argv[2]

#inputPath = "C:\\Users\divya\Dropbox\Study\IR\IRHW1\Inputfiles\\files"
#Output = "C:\\Users\divya\Desktop\Output"

clearOutput(Output)

listOfFiles = readFromDirectory()
numOfDocs = len(listOfFiles)

if not os.path.exists(Output):
    os.mkdir(Output, 0o755)
else:
    clearOutput(Output)

# print("List of files : ",listOfFiles)

i=0

allTFs = []
allfreqdicList=[]

mainDB = []
mainWordDic = []

tdmWeights = {}
tdmIndexWords = []


docAndWords = {}
##############################################main program#####################################
#From the input directory we take every single file or document, parse it through the html parser
#clean the text by removing stopwords and other uncessary expressions
###############################################################################################


for eachFile in listOfFiles:
    i+=1
    textSoupList = []
    text_soup = htmlParser(eachFile)
    stopWords = buildCustomStopwords()
    theWords = cleanText(text_soup,stopWords)
    eachFile = eachFile.replace(inputPath + "\\", "")
    eachFile = eachFile.replace(".html","")
    docAndWords[eachFile] = theWords
##############################################################################################################
#We need the name of the inputfile; such as document 001 in our postinglist output hence we fetch it from the
#input directory and remove the html extension from it
#we build a dictionary for every document with words in that document as values and document id as key
##############################################################################################################

    theWordsLength = len(theWords)
#We store the values(words) for every document in a list wordListALL
wordListAll = []
for key in docAndWords:
    wordListAll.append('\n'.join(docAndWords[key]))

theDF = buildDF(wordListAll,list(docAndWords.keys()),stop_words=None, charset_error = 'replace')
output1 = []
output2 = []
##################################Building Term-Document-Matrix#########################################################
#Using the help of Dataframes in pandas a TDM is built
#The index of this dataframe would be the words
#The columns of this dataframe would be the document id
#The cells would containa the weights of each word in a particular matrix if present
########################################################################################################################

#print(theDF)
###Setting the location to 1 as we want the position value of the word to start from 1 and not 0###
#We take the index and the
location = 1
# Below the extraction of every index(word/term) along with row( doc id and term weight in that id) is done

for o1Word, row in theDF.iterrows():
    #print('o1Word : ',o1Word)

    #print('row : ',row)
    count = 0

#Below the column (docId and weight for a corresponding term is extracted

    for col,weight in row.iteritems():
            # print('col : ',col)
            # print('weight : ',weight)

            if weight != 0.000000:
                    count+=1
                    output2.append(str(col) + ',' + str(weight))


# the word,the number of documents that contain that word (this
# corresponds to the number of records that word gets in the postings file) and the location of the first
#record for that word in the postings file is written below#############################################################
    output1.append(o1Word)
    output1.append(str(count))
    output1.append(str(location))


    location = location + count
###############################################################################################################
#Location variable carries the position of a word in the document,we add count to it so as to get the first postion
#of the next word in the postinglist
#The 2 output files the dictionary containing the word,the number of documents that contain that word (this
#corresponds to the number of records that word gets in the postings file) and the location of the first
# record for that word in the postings file and also the output file PostingList containing the document id,
#the normalized weight of the word in the document , is written onto the output directory
##############################################################################################################
writeOutput('\n'.join(output1), "dictionaryFile")
writeOutput('\n'.join(output2), "postingsFile")

###############################################################################################################
#Print the total time used for processing
###############################################################################################################

endTime = time.time()
total = endTime-startTime


print("The Total time : ",total)