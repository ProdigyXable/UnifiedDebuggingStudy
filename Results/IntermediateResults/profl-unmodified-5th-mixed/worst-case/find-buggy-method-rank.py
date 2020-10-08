import os
import sys

common_files_dir = "../common/"
variants = ["proflvariant-full-extended", "proflvariant-full-standard", "proflvariant-partial-extended", "proflvariant-standard-extended"]
 
genName = "generalSusInfo.profl"
aggName = "aggregatedSusInfo.profl"

def fetch(dirname):
    if(os.path.exists(dirname) and os.path.isdir(dirname)):
        files = os.listdir(dirname)
        if(not (genName in files)):
            print(genName, "does not exist in [exception]", dirname, sep=' ')
        if(not (aggName in files)):
            # print(aggName, "does not exist in [exception]", dirname, sep=' ')
            pass
    else:
        print(" ".join(["Directory", dirname, "does not exist [exception]"]))

def getAggRank(bm, aggRank):   
    for s in aggRank.readlines():
        lineData = s.split("|")
        if(lineData[3].strip().replace(":",".") == bm.replace(":",".")):
            return int(lineData[0])
    return 2 ** 16

def getGenRank(bm, genFile):
    for s in genFile.readlines():
        lineData = s.split("|")
        if(lineData[2].strip().replace(":",".") == bm.replace(":",".")):
            return int(lineData[0])
    return 2 ** 17

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
#---------------------------------------------------------------------#
            generalRankFile = None
            genRankFilepath = os.path.sep.join([dir, genName])
            backupGen = "/".join(dir.split("/")[-2:-1])
            backupGenPath = "/".join([common_files_dir, backupGen, genName])
#---------------------------------------------------------------------#
            aggregatedRankFile = None
            aggRankFilepath = os.path.sep.join([dir, aggName])
            backupAgg = "/".join(dir.split("/")[-2:-1])
            backupAggPath = "/".join([common_files_dir, backupAgg, aggName])
#---------------------------------------------------------------------#
            if(os.path.exists(genRankFilepath)):
                generalRankFile = open(genRankFilepath, "r")
            else:
                generalRankFile = open(backupGenPath, "r")
            gr = getGenRank(buggyMethod, generalRankFile)
            generalRankFile.close()
#---------------------------------------------------------------------#            
            if(os.path.exists(aggRankFilepath)):
                aggregatedRankFile = open(aggRankFilepath ,"r")
            else:
                aggregatedRankFile = open(backupAggPath ,"r")
            aggResult = getAggRank(buggyMethod, aggregatedRankFile)
            aggregatedRankFile.close()
#---------------------------------------------------------------------#    
            print(gr, aggResult, buggyMethod, dir, sep=',')
        except Exception as e:
            print(e)
 
main()
