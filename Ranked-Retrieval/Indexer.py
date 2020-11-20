import sys,os
import collections
from itertools import groupby
from operator import itemgetter
from collections import Counter

#get all the data from processed pages with format("page#, term")
def getData(folderName, NumFilesToProcess):
    fileList = os.listdir(str(folderName))
    desiredFiles = []
    for i in range(NumFilesToProcess):
        desiredFiles.append(fileList[i])
    #print(termSets)
    data = []
    for termSet in desiredFiles:
        terms = open("./ouputTermSets/"+str(termSet), 'r', encoding= 'utf-8')
        for term in terms:
            data.append((str(termSet.replace(".txt", "")),term.replace("\n", "")))

    return data

#termData = getData("C:/Users/steve/Desktop/Codes/School/6200/A2/ouputTermSets/")#[(termSetID, term), (termSetID, term)...]
#group data by termID, generate termIDFile format [termID term occurence]
def generateTermIDFile(folderName, NumFilesToProcess):
   
    termData = getData("./ouputTermSets/", NumFilesToProcess)
    termIDFile = [] #[[ID, [term, frequency]], [ID, [term, frequency]]...]
    ctr = collections.Counter(i[1] for i in termData)
    lst = [] #[[word, frequency]]
    sorter = sorted(termData, key=itemgetter(1))
    grouper = groupby(sorter, key=itemgetter(1))

    termDict = {k: list(map(itemgetter(0), v)) for k, v in grouper}
    frequencyList = []
    for key, value in termDict.items():
        frequencyList.append((key, len(set(value))))
    termID = 0
    for termWithFrequency in frequencyList:
        termIDFile.append([termID, [termWithFrequency[0], termWithFrequency[1]]])
        termID = termID + 1
    
    newTxt = open("./part2/" + "TermIDFile.txt", "w+", encoding='utf-8')
    for term in termIDFile:
        newTxt.write(str(term[0]) + " "+ str(term[1][0]) + " " + str(term[1][1]) + "\n")
    newTxt.close()
        
    return termDict, termIDFile
#group data by DocumentID, generate DocumentIDFile  format [pageID, [PageName, PageTokenNumber]]
def generateDocumentIDFile(folderName, NumFilesToProcess):

    termData = getData("./ouputTermSets/", NumFilesToProcess)
    sorter = sorted(termData, key=itemgetter(0))
    grouper = groupby(sorter, key=itemgetter(0))

    pageDict = {k: list(map(itemgetter(1), v)) for k, v in grouper}

    documentIDFile = []
    for key, value in pageDict.items():
        documentIDFile.append([key, [key, len(value)]])

    newTxt = open("./part2/" + "DocumentIDFile.txt", "w+", encoding='utf-8')
    for term in documentIDFile:
        newTxt.write(str(term[0]) + " "+ str(term[1][0]) + " " + str(term[1][1]) + "\n")
    newTxt.close()

    return pageDict, documentIDFile


#get the inverted collection. 
def generateInvertedCollection(folderName, NumFilesToProcess):
    
    termData = getData("./ouputTermSets/", NumFilesToProcess)
    termWithPages, termIDFile = generateTermIDFile(termData, NumFilesToProcess)
      
    invertedCollection = []
    for key, value in termWithPages.items():
        countDict = Counter(value)
        invertedCollection.append([key, countDict]) #[pageNum, {"term": 14, "term2": 12 ...}]
    tempTermID = 0
    for invertedList in invertedCollection:
        invertedList[0] = tempTermID
        tempTermID = tempTermID + 1

    newTxt = open("./part2/" + "InvertedIndex.txt", "w+", encoding='utf-8')
    newTxt.write(str(invertedCollection))
    newTxt.close()
    
    return invertedCollection #tempPostings[0][1].keys()
#print(getData("C:/Users/steve/Desktop/Codes/School/6200/A2/ouputTermSets/", 100))
# print(getData("C:/Users/steve/Desktop/Codes/School/6200/A2/ouputTermSets/"))
