import os
import sys

genName = "generalSusInfo.profl"
aggName = "aggregatedSusInfo.profl"

def fetch(dirname):
    if(os.path.exists(dirname) and os.path.isdir(dirname)):
        files = os.listdir(dirname)
        if(not (genName in files)):
            print(genName, "does not exist in [exception]", dirname, sep=' ')
            #print(" ".join([genName, "does not exist in [exception]", dirname]))
        if(not (aggName in files)):
            print(aggName, "does not exist in [exception]", dirname, sep=' ')
            #print(" ".join([aggName, "does not exist in [exception]", dirname]))
    else:
        print(" ".join(["Directory", dirname, "does not exist [exception]"]))

def getAggRank(bm, aggRank):   
    for s in aggRank.readlines():
        lineData = s.split("|")
        if(lineData[3].strip() == bm):
            return int(lineData[0])
    return -2

def getGenRank(bm, genFile):
    for s in genFile.readlines():
        lineData = s.split("|")
        if(lineData[2].strip() == bm):
            return int(lineData[0])
    return -2

def getBuggyMethods(filename):
    remove = "^^^^^^"
    file = open(filename, "r")
    result = []

    for s in file.readlines():
        result.append(s.replace(remove,"").strip())
    
        file.close()
    return result

def main():
    if(len(sys.argv) is not 3):
        print("ProFL result directory not specified, program exiting")
        return

    dir = sys.argv[1].strip()
    buggyMethodFile = sys.argv[2].strip()
    buggyMethods = getBuggyMethods(buggyMethodFile)
    for buggyMethod in buggyMethods:
        try:
            fetch(dir)

            generalRankFile = None
            genRankFilepath = os.path.sep.join([dir, genName])

            aggregatedRankFile = None
            aggRankFilepath = os.path.sep.join([dir, aggName])

            if(os.path.exists(genRankFilepath)):
                generalRankFile = open(genRankFilepath, "r")
                gr = getGenRank(buggyMethod, generalRankFile)
                generalRankFile.close()
            else:
                gr = -2
            
            if(os.path.exists(aggRankFilepath)):
                aggregatedRankFile = open(aggRankFilepath ,"r")
                aggResult = getAggRank(buggyMethod, aggregatedRankFile)
                aggregatedRankFile.close()

                if(aggResult < 0):
                    ar = gr
                else:
                    ar = aggResult
            else:
                ar = gr
    
            print(gr, ar, buggyMethod, dir, sep=',')
        except Exception as e:
            print(e)
 
main()
