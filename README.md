# Wikipedia-Search-Engine

Crawler Usage:
command line input: python3 scraper.py "seedURL" pageLimit,
for example: python3 RunCrawler.py "https://en.wikipedia.org/wiki/Stephen_Robertson_(computer_scientist)" 1000


Data Format:
termIDFile [termID term occurence]
DocumentIDFile [pageID, [PageName, PageTokenNumber]]
InvertedCollection [termID, Counter({'page#': relative occurence})], [page#, Counter({'17': relative occurence})] ..... ..]


Ranked Retrieval: 
To run the code, simply go in RunRankedRetrieval.py and run the script.
FYI Before you run, please delete Queries folder and Output.txt, then run the script.


