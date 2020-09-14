import shutil
import sys
import os

def main():
    files = []

    newPriority = int(sys.argv[1])
    
    for input in sys.argv[2:]:
        print(input)
        files.append(input)
    
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

    for file in files:
        print("--- REORDERING [START] ---")

        other = []
        unmodified = []
        reordered_output = []

        print("Processing file", file)
        file_data = open(file, "r").readlines()

        for line in file_data:
            if("PatchCategory.Unmodified" in line):
                unmodified.append(line.strip())
            else:
                other.append(line.strip())
        print(unmodified)
        print("----------")
        print(other)
        print("------------------------------")

        for message in other:
            if len(unmodified) > 0:
                if "PatchCategory.CleanFix" in message and UNMODIFIED == CLEAN:
                    mixSetup(unmodified, other, "PatchCategory.CleanFix", reordered_output)
                elif "PatchCategory.NoisyFix" in message  and UNMODIFIED == NOISY:
                    mixSetup(unmodified, other, "PatchCategory.NoisyFix", reordered_output)
                elif "PatchCategory.NoneFix" in message and UNMODIFIED == NONE:
                    mixSetup(unmodified, other, "PatchCategory.NoneFix", reordered_output)
                elif "PatchCategory.NegFix" in message and UNMODIFIED == NEG:
                    mixSetup(unmodified, other, "PatchCategory.NegFix", reordered_output)
                
            if message not in reordered_output:
                reordered_output.append(message.strip())

        if len(unmodified) > 0:
            reordered_output.extend(unmodified)
            unmodified.clear()

        print("\n".join(reordered_output))
        print("--- REORDERING [END] ---")
        rerank(file, reordered_output)
    
def mixSetup(unmodified, other, query, reordered_output):
    items = massGet(other, query)
    reordered_output.extend(mix(unmodified, items))

    for i in items:
        other.remove(i)
    unmodified.clear()

def mix(unmodified, other):
    result = []
    
    while len(unmodified) > 0 or len(other) > 0:
        if len(unmodified) > 0:
            u = unmodified[0]
            u_sbfl = float(u.split("|")[1])
        else:
            u_sbfl = float(-1)

        if len(other) > 0:
            o = other[0]
            o_sbfl = float(o.split("|")[1])
        else:
            o_sbfl = float(-1)

        if(u_sbfl > o_sbfl):
            result.append(unmodified.pop(0))
        else:
            result.append(other.pop(0))

    return result
def massGet(array, query):
    result = []
    for s in array:
        if query in s:
            result.append(s)
    return result

def rerank(file, data):
    print("--- Reranking file [START] ---")
    name = ""

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
        other = lineData[2:]
        category = lineData[2]
            
        if(getRankCategory(prevCategory) == getRankCategory(category) and prevSbfl == sbfl): 
            sameData.append(line)
        else:
            rewrite(sameData, currentRank)
            currentRank = totalRank
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

    print("--- Reranking file [END] ---")

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