import math
from DataTransformer import filterCoreList,getCoreList
import os
import glob
from UseIndex import getDocumentName, getInvertedList, getTermID, getTermIdAndInvertedList, invertedCollcetion, termIDFile, documentIDFile

invertedCollcetionDict = dict((x[0], x[1]) for x in invertedCollcetion)
termIdDict = dict((x[0], x[1]) for x in termIDFile)
documentIdDict = dict((x[0], x[1]) for x in documentIDFile)


def tokenTransform(filename):
    #keep track with index
    if not os.path.exists("Queries"):
        os.mkdir("Queries")
    f = open(str(filename), "r", encoding='utf-8')
    content = f.read().split('\n') #open Queries.txt and get the content.
    #print(str(content))
    processedQueries = []
    

    for query in content: #make each query an individual text file for DataTransformer to organize data.
        f2 = open("./Queries/"+"Query" +str(content.index(query)) +".txt", "w", encoding='utf-8')
        f2.write(query)
        f2.close()
    f.close()
    #open each query text file and perform DataTransformer operations(same as in hw2), and add them into a query list which contains[(index, processedQueryTokens), ...]
    fileList = glob.glob("./Queries/*.txt")
    for eachFile in fileList:
        processedQueries.append((fileList.index(eachFile), filterCoreList(getCoreList(eachFile))))


    return processedQueries, content



def queryWeightedTfIdf(query):
    #for each token, find tf and weighted tf(1+log_10(tf))
    weightList = []
    for token in query:
        tf = query.count(token)
        weightedTF = (1 + math.log(tf, 10))
        termID = getTermID(token)
        #documentFrequency = len(invertedCollcetionDict.get(int(termID))) #find the document frequency for the token,
        for eachTerm in termIDFile:
            if(eachTerm[0] == termID):
                documentFrequency = eachTerm[1][1]   
        idf = math.log(len(os.listdir("./ContentFolderName"))/documentFrequency, 10) #find idf = log_10(N/document frequency)
        weight = weightedTF * idf #Weight = weighted tf * idf
        weightList.append(weight)#Similarly find weights for each unique token in the query Q. 
    normalizedWeightList = []
    for eachTokenWeight in weightList: #Normalize the weights w1, w2… wn for the unique tokens in the query Q by dividing the weight w1 by sqrt (w1^2 + w2^2 … wn^2) etc.
        normalizedTokenWeight = eachTokenWeight / math.sqrt(sum([x*x for x in weightList]))
        normalizedWeightList.append(normalizedTokenWeight)

    return normalizedWeightList


def documentWeightedTfIdf(query, documentID):
    #for each token in the query Q that appears in a document, find tf for that token in the document , find weighted tf using 1 + log10(tf). 
    weightList = []
    for token in query:
        termID = getTermID(token)
        #print(termID)
        termFrequencies = invertedCollcetionDict.get(termID)
        #print(termFrequencies)
        #if int(pageID) in [int(x[0]) for x in termFrequencies.items()]:
        for key, value in termFrequencies.items():
            weight = 0
            if(int(documentID) == int(key)):
                termFrequency = value
                weightedTF = 1 + math.log(termFrequency, 10)
                idf = 1
                weight = idf * weightedTF
                break         
        weightList.append(weight)
    #print(weightList)
    normalizedWeightList = []
    for eachTokenWeight in weightList: 
        if(eachTokenWeight == 0):
            normalizedTokenWeight = 0
            normalizedWeightList.append(normalizedTokenWeight)
            continue
        normalizedTokenWeight = eachTokenWeight / math.sqrt(sum([x*x for x in weightList]))
        normalizedWeightList.append(normalizedTokenWeight)

    return normalizedWeightList
    #Assume idf = 1. Weight = weighted tf * idf for that token.
    #Similarly find weights in the document for each (unique) query token. 
    #Normalize the weights w1, w2… wn for the tokens by dividing the weight w1 by sqrt (w1^2 + w2^2 … wn^2) etc.
    

def getScore(query):
    scoreList = []
    for key in documentIdDict.keys():
        singleScore = []
        for token in query:
            queryTokenWeight = queryWeightedTfIdf(query)[query.index(token)]
            documentTokenWeight = documentWeightedTfIdf(query, key)[query.index(token)]
            product = queryTokenWeight * documentTokenWeight
            singleScore.append(product)
        if(sum(singleScore) == 0.0): #if non of the tokens appear in the document, go to the next document.
            continue
        scoreList.append((key, singleScore, sum(singleScore)))
    scoreList.sort(key=lambda x:x[2], reverse = True)
    return scoreList

    # in a for loop over the tokens in the query Q, 
    #       find the sum of the products of the corresponding normalized query 
    #       and document token weights. 
    # This sum is the score of the document D for the query Q. 
    # Do this for all (relevant) documents, find the top K documents etc.
    

#print(documentWeightedTfIdf(['annual','edinburgh','fringe','festival'], 72))
#print(str(documentIdDict))
#print(getScore(['cambridge']))
print(tokenTransform("Queries.txt"))
# f2 = open("./dict.txt", "w", encoding='utf-8')
# f2.write(str(invertedCollcetionDict))
# f2.close()