import shutil
import sys
import os

def main():
    files = []

    newPriority = int(sys.argv[1])

    name = ""

    global CLEAN
    global NOISY
    global NONE
    global NEG
    global UNMODIFIED

    CLEAN = 10000
    NOISY = 1000
    NONE = 100
    NEG = 10
    UNMODIFIED = newPriority

    for input in sys.argv[2:]:
        print(input)
        files.append(input)

    for file in files:
        print("Processing", file)
        base = os.path.sep.join(file.split(os.path.sep)[:-1])
    
        data = open(file, "r").readlines()

        currentRank = 0
        totalRank = 0
        sameData = []
        prevSbfl = 0
        prevCategory = ""

        global final_output
        final_output = []

        for line in data:
            totalRank += 1

            lineData = line.split("|")
            sbfl = float(lineData[1])

            if(len(lineData) == 4):
                category = lineData[2]
            else:
                category = ""
            
            other = lineData[2:]
            
            if(getRankCategory(prevCategory) == getRankCategory(category) and prevSbfl == sbfl): 
                sameData.append(line)
            else:
                currentRank = totalRank
                rewrite(sameData, currentRank - 1)
                sameData = []
                sameData.append(line)
            
            if(len(lineData) == 4):
                prevCategory = category
            prevSbfl = sbfl
        rewrite(sameData, totalRank)

        output = open(os.path.dirname(file) + os.path.sep + name + os.path.basename(file), "w")
        output.write("\n".join(final_output))
        output.close()

        print("Saved data to", output.name)
        print("-------------------------------")

def getRankCategory(message):

    result = -1
    if "PatchCategory.CleanFix" in message:
        result = CLEAN
    elif "PatchCategory.NoisyFix" in message:
        result = NOISY
    elif "PatchCategory.NoneFix" in message:
        result = NONE
    elif "PatchCategory.NegFix" in message:
        result = NEG
    elif "PatchCategory.Unmodified" in message:
        result = UNMODIFIED

    return result

def output(rank, sbfl, other):
    message = "|".join(["{:03d}".format(rank), "{:.6f}".format(sbfl), other])
    print(message)
    final_output.append(message)

def rewrite(data, rank):
    for line in data:
        lineData = line.split("|")
        sbfl = float(lineData[1])
        other = lineData[2:]
        output(rank, sbfl, "|".join(other).strip())

main()