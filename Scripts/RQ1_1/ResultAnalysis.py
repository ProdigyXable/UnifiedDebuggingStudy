import sys
import numpy as np
from collections import defaultdict
import utils as ut

#repair order: jGenProg GenProgA jMutRepair kParFixer RSRepair jKali KaliA Dynamoth ACS Cardumen Arja Simfix FixMiner AvatarFixer TBarFixer PraPR
#repair order: jGenProg,genprogA,jMutRepair,kPar,rsrepair,jKali,kaliA,dynamoth,acs,cardumen,arja,simfix,fixMiner,avatar,tbar,prapr
#current non plausible versions: kPar,acs,fixMiner,tbar,dynamoth,arja,jMutRepair,simfix,jKali,avatar
# no nopol anymore


def write_sbfl():
    for p in range(0, len(projects)):
        result_by_p = result_list[p]
        for r in result_by_p:
            with open("../../Results/SBFLResults/" + projects[p] + ".txt", 'a') as f:
                f.write(r + "\n")
def get_sbfl_result_list(projects):
    sbfl_result = []
    for p in range(0,len(projects)):
        result_by_p = []
        with open("../../Results/SBFLResults/" + projects[p] + ".txt") as f:
            for line in f:
                result_by_p.append(line.strip())
            sbfl_result.append(result_by_p)
    return sbfl_result
def check_result(result_list):
    check_list = []
    for p in range(0,len(result_list)):
        res = result_list[p]
        for r in range(0,len(res)):
            if not res[r].split(",")[0].isdigit():
                check_list.append(str(p) + " " + str(r))
    return check_list
def get_profl_result(projects):
    results = []
    for p in projects:
        with open("../Results/ProFLResults/final/full-results/" + p + "/a-new-1-1-max.csv") as f:
            for line in f:
                if line.startswith("STOchiai,"):
                    result = line.strip().split("STOchiai,")[1].split(",")
                    result = [float(r) for r in result]
                    results.append(result)
    return results
def get_versions(repair_tool,projects,ver, ifPlau):
    version_dic = defaultdict(list)      # all plausible versions for all projects
    with open("Results/VersionsWithCorrect/" + ifPlau + ".txt") as f:
        for line in f:
            if ":" in line:
                tool = line.split(":")[0]
                vs = line.split(":")[1].strip().replace("/","-").lower().split()
                version_dic[tool] = vs
    #deal with the specific tool
    
    plau_versions = version_dic[repair_tool.split("-")[1]]   #get plausible versions for one specific tool
    #print(plau_versions)
    
    version_list = [[] for y in range(0,len(projects))]    # for all projects
    for i in plau_versions:
        p_name = i.split("-")[0]
        p_v = i.split("-")[1]
        p_index = projects.index(p_name.capitalize())
        version_list[p_index].append(int(p_v) - 1 )
    #print(version_list)
    return version_list
def get_result_from_selected_versions(result_list,plausible_versions):
    result_list = np.array(result_list)
    new_result = []
    for i in range(0,len(result_list)):
        
        result_proj = np.array(result_list[i])
        #result_proj[plausible_versions[i]] = ''
        new_result.append(np.take(result_proj, plausible_versions[i]))
        #print(result_list[i])
    return new_result


def print_res(res,f):
    for i in range(0,len(res)):
        if isinstance(res[i], int):
            f.write(str(res[i]) + "&")
        else:
            if i < len(res) - 1:
                f.write(str(round(res[i],2)) + "&")
            else:
                f.write(str(round(res[i],2)))
def print_latex_plau(sbfl_res,profl_res,repair_tool,version_sum,ifPlau):
    with open("Results/PlauVSNonPlauLatex/" + ifPlau + "_latex.txt",'a') as f:
        f.write("\\multirow{2}{*}[-0.5ex]{" + repair_tool.split("-")[1] + "}&\\multirow{2}{*}[-0.5ex]{" + version_sum + "}&SBFL&")
        print_res(sbfl_res,f)
        f.write("\\\\" + "\n")
        f.write("&&" + "\\profl{}&")
        print_res(profl_res,f)
        f.write("\\\\" + "\n")
        f.write("\\hline" + "\n")
def write_results(res,path):
    write_path = "Results/VersionsWithCorrect/" + path + "/result.txt"

    with open(write_path,'a') as f:
        for r in res:
            f.write(str(r) + " ")
        f.write("\n")

def final_ranking_result(ver,projects, result_list):
    final_result, true_ver = ut.get_static_final(ver,projects,result_list)   # get top-1,3,5... for each projects

    final_result = ut.get_final(final_result,true_ver) #get final result (16 repair tools)
    return final_result

def write_to_csv(tool_name,final_result,result_path):
    with open(result_path,'a') as f:
        f.write(tool_name + ",")
        for i in final_result:
            i = str(i)
            if "." in i:
                f.write(str(round(float(i),2)) + ",")
            else:
                f.write(i + ",")
        f.write("\n")



tool_name_1 = ["jGenProg", "GenProgA", "jMutRepair", "kParFixer", "RSRepair", "jKali","KaliA", 
            "Dynamoth", "ACS", "Cardumen", "Arja", "Simfix", "FixMiner", "AvatarFixer", "TBarFixer","PraPR"]
tool_name_2 = ["jGenProg","genprogA","jMutRepair","kPar","rsrepair","jKali","kaliA",
            "dynamoth","acs","cardumen","arja","simfix","fixMiner","avatar","tbar","prapr"]
tool_name_list = ["jGenProg", "GenProg-A", "jMutRepair", "kPar", "RSRepair-A", "jKali","Kali-A", 
            "Dynamoth", "ACS", "Cardumen", "Arja", "Simfix", "FixMiner", "AVATAR", "TBar","PraPR"]
repair_tool = sys.argv[1]
unmodified = sys.argv[2]  # 5th, 4th, 3rd...
ifPlau = sys.argv[3]    #all results vs non-palusible versions
root_path = "../../Results/IntermediateResults/profl-unmodified-" + unmodified + "-mixed/worst-case/"
projects = ["Lang","Time","Math","Chart","Mockito","Closure"]
ver = [65,27,106,26,38,133]

sbfl_result = get_sbfl_result_list(projects)

result_list = [["" for x in range(0,ver[y])] for y in range(0,len(projects))]  #initialilize final results

for index in range(0,len(projects)):
    p = projects[index]
    result_file = root_path + "/" + repair_tool + p
    with open(result_file) as f:
        for line in f:
            items = line.split(",")
            if "exception" not in line:
                
                profl_ranking = int(items[1])
                
                proj = items[3].split("/")[-1]
                proj_id = proj.split("-")[1].strip()

                if profl_ranking < 1 :
                    continue
                else:
                    value = result_list[index][int(proj_id) - 1]
                    localization_result = items[1]
                    if value == "":
                        result_list[index][int(proj_id) - 1] = localization_result
                    else:
                        result_list[index][int(proj_id) - 1] = value + "," + localization_result
            else:
                proj_id = line.split("/")[-1].split(" ")[0].split("-")[1]
                result_list[index][int(proj_id) - 1] = sbfl_result[index][int(proj_id) - 1]

if check_result(sbfl_result) != check_result(result_list):
    print(repair_tool + " has issue!!!")

#print(result_list)


if ifPlau == "plausible" or ifPlau == "allincorrect" or ifPlau == "correct" or ifPlau == "incorrectBUTplau": #incorrect: incorrect but plausible  
    
    selected_versions = get_versions(repair_tool,projects,ver,ifPlau)
    selected_profl_result = get_result_from_selected_versions(result_list,selected_versions)  # profl result of different repair tools
    selected_sbfl_result = get_result_from_selected_versions(sbfl_result,selected_versions)
    
    profl_res, true_ver = ut.get_static_final(ver,projects, selected_profl_result) 
    sbfl_res,true_ver = ut.get_static_final(ver,projects, selected_sbfl_result) 
    
    profl_res = ut.get_final(profl_res,true_ver)
    sbfl_res = ut.get_final(sbfl_res,true_ver)

    write_results(profl_res,"profl/" + ifPlau)
    write_results(sbfl_res,"sbfl/" + ifPlau)


    version_sum = np.sum(np.array(true_ver))

    print_latex_plau(sbfl_res,profl_res,repair_tool,str(version_sum),ifPlau)
    #print(*profl_res, sep=' ')
    #print(*sbfl_res, sep=' ')
else:  # all versions
    final_result = final_ranking_result(ver,projects,result_list)
    tool_name = repair_tool.split("-")[1]
    tool_name = tool_name_list[tool_name_2.index(tool_name)]
    write_to_csv(tool_name,final_result,"../../Results/FinalResults/RQ1_1.csv")

    if tool_name == "PraPR":
        sbfl_final = final_ranking_result(ver,projects,sbfl_result)
        write_to_csv("SBFL",sbfl_final,"../../Results/FinalResults/RQ1_1.csv")
    #with open("Results/Correlation/full_results.txt",'a') as f:
    #    f.write(repair_tool.split("-")[1] + ":")
    #    for i in final_result:
    #        f.write(str(i) + " ")
    #    f.write("\n")
