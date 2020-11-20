import DataTransformer
import os
import sys
#write token line by line to file, the filename is the same as the page name that the token occured in.
def outputTerm(termSet, filename):
    newTxt = open("./ouputTermSets/" + filename.replace(".txt", "") + ".txt", "w+", encoding='utf-8')
    for term in termSet[1]:
       
        newTxt.write(term + "\n")
    newTxt.close()

#create a folder of files, the filenames are the same as pages processed from HW1. every text file contains tokens from "core" content of the wiki page.
def runTransformer(FolderName, NumFilesToProcess):
    fileList = os.listdir(str(FolderName))
    print("------------------------------------------")
    print(fileList)
    print("------------------------------------------")

    desiredFiles = []
    for i in range(NumFilesToProcess):
        desiredFiles.append(fileList[i])
    print(len(desiredFiles))
    termSets = []
    for dfile in desiredFiles:
        termSet = []
        # rawPageContent = DataTransformer.openRawHTMLsTxt()
        firstFiltered = DataTransformer.getCoreList(str(FolderName)+"/" + str(dfile))
        secondFiltered = DataTransformer.filterCoreList(firstFiltered)
        for term in secondFiltered:
            termSet.append(term)
        termSets.append((str(dfile),termSet))
    for termSet in termSets:
        outputTerm(termSet, str(termSet[0]))

    return termSets

#runTransformer("FolderName", 200)

#     f = open(str(txtName), "r",encoding='utf-8')
#     return f.read()

# command line
if __name__ == "__main__":
    folderName = str(sys.argv[1])
    limit = int(sys.argv[2])
    runTransformer(folderName, limit)