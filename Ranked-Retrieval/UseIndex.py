import Indexer
import sys,os

termData = Indexer.getData("./ouputTermSets/", len(os.listdir(str("./ouputTermSets/"))))
termWithPages, termIDFile = Indexer.generateTermIDFile(termData, len(os.listdir(str("./ouputTermSets/"))))
invertedCollcetion = Indexer.generateInvertedCollection("./ouputTermSets/", len(os.listdir(str("./ouputTermSets/"))))
pageDict, documentIDFile = Indexer.generateDocumentIDFile("./ouputTermSets/", len(os.listdir(str("./ouputTermSets/"))))\

invertedCollcetionDict = dict((x[0], x[1]) for x in invertedCollcetion)
termIdDict = dict((x[0], x[1]) for x in termIDFile)
documentIdDict = dict((x[0], x[1]) for x in documentIDFile)

def getTermID(term):
    for termID in termIDFile:
        if(str(term) == str(termID[1][0])):
            return termID[0]
            
def getInvertedList(termID):
    for invertedList in invertedCollcetion:
        if(termID == invertedList[0]):
            return invertedList[1]
    
def getTermIdAndInvertedList(term):
    termID = getTermID(term)
    for invertedList in invertedCollcetion:
        if(termID == invertedList[0]):
            return invertedList

def getDocumentName(DocumentID):
    for x in documentIDFile:
        if (int(DocumentID) == int(x[0])):
            return x[1][0]
#print(getDocumentName(123))




#test UseIndex
if __name__ == "__main__":
    typ = str(sys.argv[1])
    if(typ == "TermID"):
        print(getTermID(str(sys.argv[2])))

    elif(typ == "InvertedList"):
        print(getInvertedList(int(sys.argv[2])))

    elif(typ == "TermIdAndInvertedList"):
        print(getTermIdAndInvertedList(str(sys.argv[2])))

    elif(typ == "DocumentName"):
        print(getDocumentName(int(sys.argv[2])))
    
