import urllib3
import re
import queue
import time
import sys
# get page content in String


def getPageContent(url):
    http = urllib3.PoolManager()
    response = http.request(
        "GET", url)
    return response.data.decode("utf-8")

# get page size in int(bytes)


def getPageSize(url):
    http = urllib3.PoolManager()
    response = http.request(
        "GET", url)
    return len(response.data)

# get all the links from a wiki page without filtering


def getAllLinks(pageContent):
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', pageContent)
    linksString = (', '.join(urls))
    linksList = list(linksString.split(", "))
    return linksList

# filter obtained links from getAllLinks(url), return a list of links only contains(http://en.wikipedia.org/wiki/... without ":")


def filterLinks(links):
    rawWikis = [x for x in links if x.startswith('/wiki/')]
    filteredWikis = []
    httpWikis = []
    for x in rawWikis:
        if '#' not in x:
            if ':' not in x:
                if 'Main_Page' not in x:
                    filteredWikis.append(x)
        for y in filteredWikis:
            httpWikis.append("http://en.wikipedia.org"+y)
    return httpWikis

# write page content to txt files.


def generatePageTxt(filename, content):
    newTxt = open(str(filename)+".txt", "w", encoding='utf-8')
    newTxt.write(content)
    newTxt.close()

# write stats to a txt


def generateStatTxt(filename, maxi, mini, ave, depth):
    newTxt = open(filename+".txt", "w")
    newTxt.write("Maximum size: " + str(maxi) + "bytes\n")
    newTxt.write("Minimum size: " + str(mini) + "bytes\n")
    newTxt.write("Average size: " + str(ave) + "bytes\n")
    newTxt.write("Max Depth Reached: " + str(depth))
    newTxt.close()


# crawler start to crawl
def crawler(seedUrl, numPages):
    startTime = time.time()
    allCrawledPages = []  # document all the crawled pages
    pageStats = []
    depthLimit = 5
    depthCount = 0
    pageCount = 0

    pageFrontier = []  # setup a frontier for new links.
    pageFrontier.append(seedUrl)  # first link is the seed URL.
    while depthCount < depthLimit:  # set up depth limit for crawler.
        # set up depth cache to store new links so the list that is being iterated over wont be overwritten to avoid potential bugs.
        depthCache = []
        for x in pageFrontier:  # for every link in each depth.
            # time.sleep(0.1)  # politeness
            pageContent = getPageContent(x)
            generatePageTxt(pageCount, pageContent)
            pageStats.append(len(pageContent.encode("utf-8")))
            allLinks = getAllLinks(pageContent)
            httpWikis = filterLinks(allLinks)
            for httpWiki in httpWikis:
                depthCache.append(httpWiki)  # add new links to cache.
            # check if there's duplicated links comparing to crawled list.
            if x not in allCrawledPages:
                allCrawledPages.append(x)  # if new, add to crawled list.
                pageCount = pageCount + 1  # crawled page # +1.
            if pageCount == numPages:  # if reach limit,
                end1 = time.time()
                # write all crwaled link to a txt.
                with open('URLsCrawled.txt', 'w') as f:
                    for page in allCrawledPages:
                        f.write("%s\n" % page)
                generateStatTxt("Stats", max(pageStats), min(  # write stats to a txt.
                    pageStats), sum(pageStats)/len(pageStats), (depthCount+1))
                print("Maximam Depth Reached: "+str(depthCount+1) +  # print out stats.
                      ", Page Crawled: " + str(pageCount) +
                      ", Maximum size: " + str(max(pageStats)) + "bytes" +
                      ", Minimum size: " + str(min(pageStats)) + "bytes" +
                      ", Average size: " + str(sum(pageStats)/len(pageStats)) + "bytes" +
                      ", Time used: " + str(end1 - startTime) + "seconds")

                return (depthCount, pageCount, max(pageStats), min(pageStats), sum(pageStats)/len(pageStats))
        temp = []
        for x in depthCache:
            if x not in allCrawledPages:  # check if "new" links have duplicates in crawled list.
                temp.append(x)  # if not added to temp.
        # let the frontier be the temp, prepare for next depth.
        pageFrontier = list(set(temp))  # use set to remove duplicates.
        depthCount = depthCount + 1
    end2 = time.time()
    with open('URLsCrawled.txt', 'w') as f:
        for page in allCrawledPages:
            f.write("%s\n" % page)
    generateStatTxt("Stats", max(pageStats), min(
                    pageStats), sum(pageStats)/len(pageStats), (depthCount+1))
    print("Maximam Depth Reached: "+str(depthCount+1) +
          ", Page Crawled: " + str(pageCount) +
          ", Maximum size: " + str(max(pageStats)) + "bytes" +
          ", Minimum size: " + str(min(pageStats)) + "bytes" +
          ", Average size: " + str(sum(pageStats)/len(pageStats)) + "bytes" +
          ", Time used: " + str(end2 - startTime) + "seconds")
    return (depthCount, pageCount, max(pageStats), min(pageStats), sum(pageStats)/len(pageStats))


crawler("https://en.wikipedia.org/wiki/Stephen_Robertson_(computer_scientist)", 1000)
# command line
# if __name__ == "__main__":
#     seed = sys.argv[1]
#     limit = int(sys.argv[2])
#     crawler(seed, limit)
#crawler("https://en.wikipedia.org/wiki/Stephen_Robertson_(computer_scientist)", 1000)
# print(len(getPageContent(
#     "https://en.wikipedia.org/wiki/Stephen_Robertson_(computer_scientist)").encode("utf-8")))
# print(getPageSize(
#     "https://en.wikipedia.org/wiki/Stephen_Robertson_(computer_scientist)"))
