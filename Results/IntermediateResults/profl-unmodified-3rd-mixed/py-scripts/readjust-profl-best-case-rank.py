import shutil
import sys
import os

def main():
    files = []

    name = ""

    for input in sys.argv[1:]:
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
            category = lineData[2]
            other = lineData[2:]
            
            if(prevCategory == category and prevSbfl == sbfl):  
                sameData.append(line)
            else:
                rewrite(sameData, currentRank)
                currentRank = totalRank
                sameData = []
                sameData.append(line)

            if(len(lineData) == 4):
                prevCategory = category
            prevSbfl = sbfl
        rewrite(sameData, totalRank - 1)

        output = open(os.path.dirname(file) + os.path.sep + name + os.path.basename(file), "w")
        output.write("\n".join(final_output))
        output.close()

        print("Saved data to", output.name)
        print("-------------------------------")

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