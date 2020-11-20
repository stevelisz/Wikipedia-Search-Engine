import Indexer
import sys

def createIndex(folderName, numFilesToProcess):
    Indexer.generateTermIDFile(folderName, numFilesToProcess)
    Indexer.generateDocumentIDFile(folderName, numFilesToProcess)
    Indexer.generateInvertedCollection(folderName, numFilesToProcess)

if __name__ == "__main__":
    folderName = str(sys.argv[1])
    limit = int(sys.argv[2])
    createIndex(folderName, limit)
    