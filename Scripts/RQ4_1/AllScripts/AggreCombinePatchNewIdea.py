import sys
from collections import defaultdict
import numpy as np
import os
sys.path.append("../../RQ1_1/")
import utils as ut
import getAllPatchCount as ut2
import UnidebugUtil as uniutil

def write_data(method_name, value, path):
    with open(path,'a') as f:
        f.write(method_name + " " + str(value))
        f.write("\n")



def get_current_SBFL_value(file):
    sus_dic = dict() 
    if os.path.exists(file):   
        with open(file) as f:
            for line in f:
                method_name = line.split("  ")[0]
                value = line.split("  ")[1].strip()
                sus_dic[method_name.replace(":",".")] = value
    return sus_dic

def store_cate_each_tool(method_name,cate,path):
    if not os.path.exists(path):
        os.makedirs(path)

    file = path + "/" + proj + "-" + ver +".txt"
    with open(file,'a+') as f:
        f.write(method_name + " " + cate)
        f.write("\n")



def get_basic(tool_combs,single_tool_base_path,proj,ver,mix_unmodified,SBFL_sus_values,sbfl_formula):
    method_cate = defaultdict(list) #index of Unmodified_ranking
    method_value = dict()      #suspicious value
    method_clean = defaultdict(list) # real category list
    for tool in tool_combs:
        if not os.path.exists(single_tool_base_path + tool):
            print(single_tool_base_path + tool + "DOES NOT EXISIT!")
        result_file = single_tool_base_path + tool + "/" + proj + "-" + ver + "/aggregatedSusInfo.profl"

        if os.path.exists(result_file):
            with open(result_file) as f:
                for line in f:
                    items = line.strip().split("|")
                    method_name = items[3]
                    cate = items[2].split("PatchCategory.")[1]
                    if cate == "Unmodified":
                        cate = mix_unmodified
                    #value = items[1]
                    method_name = method_name.replace(":",".")
                    if method_name.replace(":",".") in SBFL_sus_values:
                            value = SBFL_sus_values[method_name.replace(":",".")]
                            method_cate[method_name].append(unmodified_ranking.index(cate))
                            method_clean[method_name].append(cate)
                            method_value[method_name] = value


                            store_cate_each_tool(method_name,cate, 
                                "/home/xia/T/TSEUniDebug/UnifiedDebuggingStudy67a46b0/Data/BaseData/CategoryEachTool/" + tool )

                            folder = "../../Data/DeepFLData/SusValue/" + sbfl_formula
                            if not os.path.exists(folder):
                                os.makedirs(folder)
                              
                            #write_data(method_name,value,folder + "/" + ver + "-" + proj + ".txt")

                    
    return method_cate,method_value,method_clean

#method_cate_number: number of tool category,for example, if M1 aggregation is
#cleanfix, count how many tools are also cleanfix for M1
def get_method_info(counts_dict,method_cate,method_value,method_clean,ver,proj,sbfl_formula):
    method_final_cate = dict()   # final category
    method_cate_number = dict() # number of cleanfix/Noisyfix/NoneFix for all tools
    for m in method_cate:
        m = m.replace(":",".")
        min_number = np.array(method_cate[m]).min()
        cat = unmodified_ranking[min_number] #the aggregated category for this method
        method_final_cate[m] = cat
        cat_list = method_clean[m]
        #cat_number = cat_list.count(cat)  #use number of tools
        cat_number = counts_dict[m.replace(":",".")][min_number]  # use number of all patches
        if cat_number > 0:
            method_cate_number[m.replace(":",".")] = cat_number
            
            #Store information
            folder1 = "../../Data/DeepFLData/Category/" + sbfl_formula
            folder2 = "../../Data/DeepFLData/CategoryNumber/" + sbfl_formula
            if not os.path.exists(folder1):
                os.makedirs(folder1)
            if not os.path.exists(folder2):
                os.makedirs(folder2)
            #write_data(m,cat,folder1 + "/" + ver + "-" + proj + ".txt")
            #write_data(m,cat_number,folder2 + "/" + ver + "-" + proj + ".txt")
            ###
    return method_final_cate,method_cate_number

def get_info_for_ranking(method_value,method_final_cate,method_clean_number):
    category_values = defaultdict(list)  #each category with a list of suspicious values
    for m in method_final_cate:
        category_values[method_final_cate[m]].append(float(method_value[m]))
    return category_values

def get_buggy(buggy_method_path):
    buggy = []
    with open(buggy_method_path) as f:
        for line in f:
            if  "^^^^^^" in line:
                buggy.append(line.split("^^^^^^")[1].strip().replace(":","."))
    return buggy

def update_ranking_by_cate_number(cate_number_dict,bug,method_cate_number,method_value,method_final_cate):
    offset = 0
    if bug in method_cate_number:
        bug = bug.replace(":",".")
      
        bug_cate_number = method_cate_number[bug]
        bug_value = method_value[bug]
        bug_cate = method_final_cate[bug]

        cate_number_list = np.sort(np.array(cate_number_dict[bug_cate + "+" + bug_value]))
        offset = list(cate_number_list).index(bug_cate_number)
    return offset

def get_final_ranking(buggy_methods,method_final_cate,method_value,unmodified_ranking,category_values,buggy_SBFL_ranking,cate_number_dict,method_cate_number):
    rankings = []
    global unidebug_plusplus
    for bug in buggy_methods:
        bug = bug.replace(":",".")
        if bug in method_value:
            
            bug_cat = method_final_cate[bug]
            bug_valu = float(method_value[bug])
            bug_ranking = 0
            for m in unmodified_ranking:

                if bug_cat != m:
                    bug_ranking = bug_ranking + len(category_values[m])            
                else:
                    m_list = category_values[m]
                    m_list = np.array(m_list)
                    m_list_sort = np.sort(m_list) #ascending order
                    index = list(m_list_sort).index(bug_valu)
                    bug_ranking = len(m_list_sort) - index + bug_ranking

                    offset = update_ranking_by_cate_number(cate_number_dict,bug,method_cate_number,method_value,method_final_cate)

                    #if(unidebug_plusplus is "False"):
                    #    pass # When the third command argument is "False", output represents UniDebug+
                    #else:
                    bug_ranking = bug_ranking - offset # Comment this line to change from UniDebug++ to UniDebug+

                    rankings.append(str(bug_ranking))
                    
        else:    
        
        
     
            bug = bug.replace(":",".")

            if bug in buggy_SBFL_ranking:
                rankings.append(buggy_SBFL_ranking[bug])

    return rankings

def get_SBFL_ranking_OLD(single_tool_base_path,buggy_methods,proj,ver):
    buggy_SBFL_ranking = dict()
    attempts = ["FixMiner/"]
    
    stop = False    

    for tool in attempts:
        if not stop:
            try:
                file = single_tool_base_path + tool + proj + "-" + ver + "/generalSusInfo.profl" 
                with open(file) as f:
                    for line in f:
                        method_name = line.split("|")[2].strip()
                        if method_name in buggy_methods:
                            value = line.split("|")[0].lstrip("0")
                            buggy_SBFL_ranking[method_name] = value
                            stop = True
            except Exception as e:
                print(e)
                pass
    return buggy_SBFL_ranking

# get the dict: (category + susvalue):[1,2,3,4] "1,2,3,4" represent the number
# of tools with same category as buggy method
# For example, buggy-method-1 will have 3 tools assinging nonfix to it,
# 2 represents that for another method-2 (also nonefix) has 2 tools assinging
# nonefix to method-2
# And buggy-method-1 and method-2 has the same susvalue
def get_cate_number_info(buggy_methods,method_final_cate,method_value,method_cate_number):
    cate_meth_dict = defaultdict(set)   # value:set(meth1,meth2,meth3...)
    for buggy_m in buggy_methods:  #all bugs
        buggy_m = buggy_m.replace(":",".")
        if buggy_m in method_value:
            buggy_value = method_value[buggy_m]            
            buggy_cat = method_final_cate[buggy_m]
            for meth in method_value:
                meth = meth.replace(":",".")
                if buggy_value == method_value[meth] and buggy_cat == method_final_cate[meth]:                                
                    cate_meth_dict[buggy_cat + "+" + str(buggy_value)].add(meth)
    
    cate_number_dict = defaultdict(list)
    #print(method_cate_number)
    for cat_and_value in cate_meth_dict:
        mtd_list = cate_meth_dict[cat_and_value]
        for mtd in mtd_list:
            if mtd.replace(":",".") in method_cate_number:
                cate_number_dict[cat_and_value].append(method_cate_number[mtd.replace(":",".")]) 
    return cate_number_dict

def read_comb(comb_file):
    co_list = []
    with open(comb_file) as f:
        for line in f:
            co_list.append(line.strip())
    return co_list

def write_results(result_list,comb_file,comb,max_top1):
    global first_write
    with open(comb_file + ".result",'a') as f:
        if(first_write is False):
            first_write = True
            f.write("<Format = Top1 Top3 Top5 MFR MAR from Tool(s)>")
            f.write("\n")
        if int(result_list[0]) > max_top1:    
            value = int(result_list[0])
            print("\t- Best Top1 found! (previous max vs now)", str(max_top1), value)
            max_top1 = value
        
        for r in result_list:
            f.write(str(r) + " ")
        f.write(" " + comb)
        f.write("\n")
    return max_top1

def get_SBFL_ranking(file, buggy_methods):
    buggy_SBFL_ranking = dict()

    if os.path.exists(file):

        with open(file) as f:
            for line in f:
                m = line.split("  ")[0]

                ranking = line.split("  ")[1].strip()
                buggy_SBFL_ranking[m.replace(":",".")] = ranking

    return(buggy_SBFL_ranking)
def write_result_for_RQ3(result_list,tool_combs):
    file = "../RQ1_1/SingleToolResults/" + tool_combs[0] + ".txt"
    with open(file,'a+') as f:
        for p in result_list:
            for res in p:
                f.write(res + "|")
            f.write("\n")
def write_result_to_csv(path,result_list,projects):
    with open(path,'a+') as f:
        for p_indx in range(0,len(result_list)):
            p_name = projects[p_indx]
            for v_idx in range(0,len(result_list[p_indx])):
                version = str(v_idx + 1)
                f.write(p_name + "-" + version)
                f.write(",")
                f.write(result_list[p_indx][v_idx].replace(",","|"))
                f.write("\n")



first_write = False
single_tool_base_path = "../../../Data/ExperimentalData/ProFL-"

#projects = ["Lang","Time","Math","Chart","Mockito","Closure"]
#vers = [65,27,106,26,38,133]

#projects = ["Lang","Time","Math","Chart"]
#vers = [65,27,106,26]

#projects = ["Closure"]
#vers = [133]

#projects = ["Mockito"]
#vers = [38]

projects = ["Mockito","Closure"]
vers = [38,133]



comb_file = sys.argv[1] #what tools for aggregation: for example, "SimFix PraPR FixMiner"
mix_unmodified = sys.argv[2]  #four mixed options: "CleanFix","NoisyFix","NoneFix","NegFix"
unidebug_plusplus = "True"

if(len(sys.argv) > 3):
    unidebug_plusplus = sys.argv[3]

sbfl_formula = sys.argv[4]   # formula such as: "STOchiai"

unmodified_ranking = ["CleanFix","NoisyFix","NoneFix","NegFix"]

combs_from_file = read_comb(comb_file)
max_top1 = 0
index = 0

for comb in combs_from_file:
    result_list = [["" for x in range(0,vers[y])] for y in range(0,len(projects))]  #initialilize final results
    tool_combs = comb.split()




    for current_iteration_number in range(0,len(projects)):   #each project
        proj = projects[current_iteration_number]
        vs = vers[current_iteration_number]

        for ver in range(1,vs + 1):
            
                counts_dict = uniutil.get_all_patch_number(tool_combs,proj,ver)
            
                
                ver = str(ver)
                #print(proj + "-" + ver)
                buggy_method_path = "../../../Data/FaultyMethods/" + proj + "/" + ver + ".txt"

                buggy_methods = get_buggy(buggy_method_path)
                #buggy_SBFL_ranking = get_SBFL_ranking_OLD(single_tool_base_path,buggy_methods,proj,ver)
                buggy_SBFL_ranking = get_SBFL_ranking("../../../Results/SBFLRelated/SBFLBugRanks/" + sbfl_formula + "/" + proj + "-" + ver + ".txt",buggy_methods)
                SBFL_sus_values = get_current_SBFL_value("../../../Results/SBFLRelated/SBFLSusValues/" + sbfl_formula + "/" + proj + "-" + ver + ".txt")
                method_cate,method_value,method_all_cate = get_basic(tool_combs,single_tool_base_path,proj,ver,mix_unmodified,SBFL_sus_values,sbfl_formula)
                method_final_cate,method_cate_number = get_method_info(counts_dict,method_cate,method_value,method_all_cate,ver,proj,sbfl_formula) 

                cate_number_dict = get_cate_number_info(buggy_methods,method_final_cate,method_value,method_cate_number)

                category_values = get_info_for_ranking(method_value,method_final_cate,method_cate_number)
                
                final_ranking = get_final_ranking(buggy_methods,method_final_cate,method_value,unmodified_ranking,category_values,buggy_SBFL_ranking,cate_number_dict,method_cate_number)
                final_r_string = ",".join(final_ranking)
                result_list[current_iteration_number][int(ver) - 1] = final_r_string
            #except:
            #    pass
                #print("Could not process", projects[index], proj, "-" ,ver)

    print(result_list)
    final_result, true_ver = ut.get_static_final(vers,projects,result_list)   # get top-1,3,5...  for each projects
    final_result = ut.get_final(final_result,true_ver) #get final result (16 repair tools)
    
    index = index + 1
    #print("Combination", index, "metric results =", final_result)
    #print(sbfl_formula,end = " ")
    print(tool_combs[0],end = " ")  
    print(*final_result) 
    #max_top1 = write_results(final_result,comb_file,comb,max_top1)
    #write_result_for_RQ3(result_list,tool_combs)

    #write_result_to_csv("./ASEResults/" + tool_combs[0] + ".csv",result_list,projects)
    #with open("ClosureAndMockitoUnidebug.txt",'a+') as f:
    #    f.write(tool_combs[0] + "|")
    #    for pro_res in result_list:
    #        for j in pro_res:
    #            f.write(j + "|")
    #    f.write("\n")

