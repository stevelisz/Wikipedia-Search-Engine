import RankedRetrieval 
import DataTransformer

def runner(IndexFolderName, ContentFolderName, QueriesTxtName, K):
    f = open("./Output.txt", "w", encoding='utf-8')
    
    queries, content = RankedRetrieval.tokenTransform(str(QueriesTxtName))
    for query in queries:
        f.write(str(content[queries.index(query)]) + "\n") #write raw query
        f.write(str(query[1]) + "\n") #write toeknized and data transformed query
        scoreList = RankedRetrieval.getScore(query[1])
    
        if(len(scoreList) < int(K)):
            for score in scoreList:
                f.write(str(score[0])+"  "+str(score[0]) + "\n") #write documentID <tab> documentName

                
                somewhatCoreContent = DataTransformer.getCoreList("./" +str(ContentFolderName)+"/"+str(score[0])+".txt")
                filteredContent = DataTransformer.filterCoreList(somewhatCoreContent)
                snippet = str(filteredContent)[:200]
                f.write(snippet + "\n") #write first 200 bytes

                f.write(str(score[2])+"\n") #write score
                for token in query[1]:
                    f.write(str(token) + ": " + str(score[1][query[1].index(token)]) + " ")
                # f.write(str(query[1][0]) + ": "+ str(score[1][0]) + " "
                # + str(query[1][1]) + ": "+ str(score[1][1]) + " "
                # + str(query[1][2]) + ": "+ str(score[1][2]) + " "
                # + str(query[1][3]) + ": "+ str(score[1][3]) + "\n") #write contribution

                f.write("\n")

        if(len(scoreList) >= int(K)):
            for i in range(K):
                f.write(str(scoreList[i][0])+"  "+str(scoreList[i][0]) + "\n") #write documentID <tab> documentName

                somewhatCoreContent = DataTransformer.getCoreList("./" +str(ContentFolderName)+"/"+str(scoreList[i][0])+".txt")
                filteredContent = DataTransformer.filterCoreList(somewhatCoreContent)
                snippet = str(filteredContent)[:200]
                f.write(snippet + "\n") #write first 200 bytes
                
                f.write(str(scoreList[i][2])+"\n") #write score
                for token in query[1]:
                    f.write(str(token) + ": " + str(scoreList[i][1][query[1].index(token)]) + " ")

                # f.write(str(query[1][0]) + ": "+ str(scoreList[i][1][0]) + " " 
                # + str(query[1][1]) + ": "+ str(scoreList[i][1][1]) + " "
                # + str(query[1][2]) + ": "+ str(scoreList[i][1][2]) + " "
                # + str(query[1][3]) + ": "+ str(scoreList[i][1][3]) + "\n") #write contribution

                f.write("\n")

        f.write("\n")
        f.write("\n")
    f.close()

runner("IndexFolderName", "ContentFolderName", "Queries.txt", 15)
# queries, content = RankedRetrieval.tokenTransform("Queries.txt")
# print(queries)