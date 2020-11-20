import re
import os
from string import punctuation


#read HTML file
def openRawHTMLsTxt(txtName):
    f = open(str(txtName), "r",encoding='utf-8')
    return f.read()

#trying to remove unnecessary content such as footer, style, script from the HTML
#return a list of unfiltered tokens
def getCoreList(singleHTML):
    rawContent = openRawHTMLsTxt(singleHTML)
    navRemoved = re.sub(
        '<nav[^>]*>\s*((?:.|\n)*?)</nav>', '\n', rawContent)
    styNavRemoved = re.sub('<style[^>]*>\s*((?:.|\n)*?)</style>', '\n', navRemoved)
    scrStyNavRemoved = re.sub(
        '<script[^>]*>\s*((?:.|\n)*?)</script>', '\n', styNavRemoved)
    fooScrStyNavRemoved = str(
        re.sub('<footer[^>]*>\s*((?:.|\n)*?)</footer>', '\n', scrStyNavRemoved))
    somewhatCoreContent = str(re.sub('<[^>]*>', '\n', fooScrStyNavRemoved))
    result = ' '.join(somewhatCoreContent.split())
    result = result.replace(' ', '\n')
    lst = result.split("\n")
    return lst


#filter the tokens, split them further more if not clean with puncuation.
#perform required such as remove "'", split numbers etc.,
#return a list of cleaned tokens
def filterCoreList(coreList):
    lowerList = [x.lower() for x in coreList]
    symbolElementRemoved = []

    for i in range(len(lowerList)):  #cleaning tokenzied content
        if(lowerList[i].find("(") != -1):
            lowerList[i] = lowerList[i].replace("(", "")
        if(lowerList[i].find(")") != -1):
            lowerList[i] = lowerList[i].replace(")", "")
        if(lowerList[i].find("'") != -1):
            lowerList[i] = lowerList[i].replace("'", "")
        if(lowerList[i].find(";") != -1):
            lowerList[i] = lowerList[i].replace(";", "")
        if(lowerList[i].find(":") != -1):
            lowerList[i] = lowerList[i].replace(":", "")
        if(lowerList[i].find("!") != -1):
            lowerList[i] = lowerList[i].replace("!", "")
        if(lowerList[i].find("?") != -1):
            lowerList[i] = lowerList[i].replace("?", "")
        if(lowerList[i][:1].isalpha() and lowerList[i].find(".") != -1):
            lowerList[i] = lowerList[i].replace(".", "")
        if(lowerList[i][:1].isalpha() and lowerList[i].find(",") != -1):
            lowerList[i] = lowerList[i].replace(",", "")
        if(lowerList[i][:1].isalpha() and lowerList[i].find('"') != -1):
            lowerList[i] = lowerList[i].replace('"', "")
        
        
        symbolElementRemoved.append(lowerList[i])
    clean1 = []    
    for element in symbolElementRemoved:
        if(not element[:1].isalnum()):
            continue
        clean1.append(element)


    
    clean2 = []
    for j in range(len(clean1)):
        if(re.match('^(?=.*[0-9])(?=.*[a-zA-Z])', clean1[j])): #clean odd combination
            continue
        
        if(re.match('([0-9]+[,.]+[0-9]+)', clean1[j])): #seperate numbers with comma or dot
            tempValue = clean1[j].replace(".",",")
            tempSplit = tempValue.split(",")
            clean2.extend(tempSplit)
            continue
        clean2.append(clean1[j])
            
    return clean2




# print(getBodyContent("FolderName/23.txt"))
coreContent = getCoreList("FolderName/0.txt")
# lst = coreContent.split("\n")
test = ["999,999,999", "55.2,2.312", "&@#!@$", "3D", "I.B.M.", "s.teve's", "sdas","sbsb.sbs", "asdd$@#213sdas,", ".Net", "1a2b4c", "&#28139"]
print(filterCoreList(test))

# if("12.4"[0].isalpha()):  #"([0-9]+[,.]+[0-9]+)"
#     print("true")
# newTxt = open("test.txt", "w")
# newTxt.write(getBodyContent("FolderName/0.txt"))
# newTxt.close()

