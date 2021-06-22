import sys
import copy
sys.path.append("../RQ1_1/")

from collections import defaultdict

import numpy as np
import os
import utils as ut

def get_current_SBFL_value(file):
    sus_dict = dict() 

    if os.path.exists(file):   
        with open(file) as f:
            for line in f:
                method_name = line.split()[0].replace(":",".")
                value = line.split()[1].strip()
                sus_dict[method_name] = value
    return sus_dict

def getProperMethodName(statement_level, method_name):
    if statement_level == "Method":
        return_value = method_name.replace(":",".").strip()
    
    elif statement_level == "Statement":
        if "#" in method_name:
            return_value = method_name.split(":")[0] + ":" + method_name.split("#")[1]  # Actual statement
            return_value = return_value.replace(":",".").strip()
    return return_value
    
def get_basic(tool_combs, single_tool_base_path, proj, ver, unmodified_category, SusValues, sbfl_formula, profl_variant, statement_level):
    global cachedGeneralSus
    global cachedAggregatedSus
    global cachedMethodCount 

    proj_name = proj + "-" + ver
    
    if proj_name in cachedGeneralSus.keys():
        method_category = copy.deepcopy(cachedGeneralSus[proj_name][0])
        method_all_category = copy.deepcopy(cachedGeneralSus[proj_name][1])
        method_value = copy.deepcopy(cachedGeneralSus[proj_name][2])
    else:
        method_category = defaultdict(list) #index of Unmodified_ranking
        method_all_category = defaultdict(list) # real category list
        method_value = dict() # suspicious value
    
        if statement_level == "Method":
            general_file = single_tool_base_path + "../common/" + proj + "-" + ver +  "/generalSusInfo.profl"
            # ----- Get suspicious values from common files ----- #
            if os.path.exists(general_file):
                g = open(general_file, "r")

                for line in g:
                    items = line.strip().split("|")

                    mRank = items[0]
                    mSus = items[1]
                    mName = items[2].replace(":",".").strip()
                 
                    # ------ Added unmodified category to all methods----- #
                    if float(mSus) > 0.0:
                        method_category[mName].append(category_indices.index(unmodified_category))
                        method_all_category[mName].append(unmodified_category)
                        method_value[mName] = mSus
            else:
                print("Missing", general_file)
        elif statement_level == "Statement":
            for mName in sorted(SusValues.keys()):
                if float(SusValues[mName]) > 0.0:
                    method_category[mName].append(category_indices.index(unmodified_category))
                    method_all_category[mName].append(unmodified_category)
                    method_value[mName] = SusValues[mName]

        cachedGeneralSus[proj_name] = dict()
        cachedGeneralSus[proj_name][0] = copy.deepcopy(method_category)
        cachedGeneralSus[proj_name][1] = copy.deepcopy(method_all_category)
        cachedGeneralSus[proj_name][2] = copy.deepcopy(method_value)

    # ----- Add AggregatedSusInfo Data ----- #
    accumulated_method_count = defaultdict(int)

    for tool in tool_combs:
        repeatedKeys = list()
        tool_proj_name = tool + "-" + proj_name
        
        # ----- Add category_information data----- #
        if tool_proj_name in cachedMethodCount.keys():
            pass
        else:
            cachedMethodCount[tool_proj_name] = defaultdict(int)

            cat_info_file_path = single_tool_base_path + "ProFL-" + tool + "/" + proj + "-" + ver + "/proflvariant-" + profl_variant + "/category_information.profl"
            try:
                cat_info_file = open(cat_info_file_path, "r")
    
                for cat_line in cat_info_file:
                    cat_line = cat_line.strip()
                    if "PatchCategory" in cat_line:
                        pass
                    else:
                        cat_line_data = cat_line.split(" = ")
                        cat_line_data[0] = getProperMethodName(statement_level, cat_line_data[0])
                        if not cat_line_data[0] in repeatedKeys:
                            if not cat_line_data[0] in cachedMethodCount[tool_proj_name].keys():
                                cachedMethodCount[tool_proj_name][cat_line_data[0]] = 0
                            cachedMethodCount[tool_proj_name][cat_line_data[0]] = int(cat_line_data[1]) + cachedMethodCount[tool_proj_name][cat_line_data[0]]
                            #repeatedKeys.add(cat_line_data[0])
            except:
                pass

        for methodSig in cachedMethodCount[tool_proj_name].keys():
            accumulated_method_count[methodSig] = accumulated_method_count[methodSig] + cachedMethodCount[tool_proj_name][methodSig]
    
        # ----- Get actual AggregatedSusInfo information ----- #
        if tool_proj_name in cachedAggregatedSus.keys():
            for key in copy.deepcopy(cachedAggregatedSus[tool_proj_name][0]):
                method_category[key].extend(copy.deepcopy(cachedAggregatedSus[tool_proj_name][0][key]))

            for key in copy.deepcopy(cachedAggregatedSus[tool_proj_name][1]):
                method_all_category[key].extend(copy.deepcopy(cachedAggregatedSus[tool_proj_name][1][key]))

            method_value.update(copy.deepcopy(cachedAggregatedSus[tool_proj_name][2]))

        else: 
            if not os.path.exists(single_tool_base_path + "ProFL-" + tool):
                print("Missing tool path", single_tool_base_path, "ProFL-" + tool)
            if tool == "TBarFixer":
                pass
                #single_tool_base_path = "/media/disk2/sam/TSE-data/UnifiedDebuggingStudy/Results/ASE-Data-new/"

            ase_path = "/media/disk2/sam/ASE-data/proflstudy/ResultsFromSam/profl-unmodified-4th-mixed/worst-case/" # ASE-DATA
            aggregated_file = single_tool_base_path + "ProFL-" + tool + "/" + proj + "-" + ver + "/proflvariant-" + profl_variant + "/aggregatedSusInfo.profl"
            #aggregated_file = ase_path + "ProFL-" + tool + "/" + proj + "-" + ver + "/aggregatedSusInfo.profl"
            cachedAggregatedSus[tool_proj_name] = dict()
            cachedAggregatedSus[tool_proj_name][0] = copy.deepcopy(cachedGeneralSus[proj_name][0])
            cachedAggregatedSus[tool_proj_name][1] = copy.deepcopy(cachedGeneralSus[proj_name][1])
            cachedAggregatedSus[tool_proj_name][2] = copy.deepcopy(cachedGeneralSus[proj_name][2])

            # ----- Add information to dict ----- #
            if os.path.exists(aggregated_file):
                with open(aggregated_file, "r") as f:
                    for line in f:
                        items = line.strip().split("|")
                        method_name = items[3].strip()
                        category = items[2].split("PatchCategory.")[1]

                        # --- Set sus value --- #
                        value = 0

                        if statement_level == "Method":
                            method_name = getProperMethodName(statement_level, method_name)

                            if method_name in method_value.keys():
                                value = method_value[method_name]
    
                        elif statement_level == "Statement":
                            if "#" in method_name:
                                method_name = getProperMethodName(statement_level, method_name)
    
                                if method_name in SusValues.keys():
                                    value = SusValues[method_name]
                            else:
                                continue
                        if float(value) > 0.0:
                            cachedAggregatedSus[tool_proj_name][0][method_name].append(category_indices.index(category))
                            cachedAggregatedSus[tool_proj_name][1][method_name].append(category)
                            cachedAggregatedSus[tool_proj_name][2][method_name] = value

                            method_category[method_name].append(category_indices.index(category))
                            method_all_category[method_name].append(category)
                            method_value[method_name] = value

    return method_category, method_value, method_all_category, accumulated_method_count

# method_category_number: number of tool category, for example, if M1 aggregation is CleanFix, count how many tools are also CleanFix for M1
def get_method_info(method_category, method_value, method_all_category, ver, proj, sbfl_formula):
    method_final_category = dict() # final category
    method_category_number = dict() # number of cleanfix/Noisyfix/NoneFix for all tools
    method_final_category_index = dict()

    for m in method_category:
        min_number = np.array(method_category[m]).min()
        cat = category_indices[min_number] # The aggregated category for this method
        method_final_category[m] = cat
        cat_list = method_all_category[m]
        cat_number = cat_list.count(cat)
        
        method_final_category_index[m] = min_number
        method_category_number[m] = cat_number
    return method_final_category, method_category_number, method_final_category_index

def get_info_for_ranking(method_value, method_final_category, method_all_category_number):
    category_values = defaultdict(list)  # Each category with a list of suspicious values

    for m in method_final_category:
        category_values[method_final_category[m]].append(float(method_value[m]))
    return category_values

def get_buggy(buggy_method_path):
    buggy = []
    with open(buggy_method_path) as f:
        for line in f:
            if  "^^^^^^" in line:
                buggy.append(line.split("^^^^^^")[1].strip().replace(":","."))
    return buggy

def get_buggy_statment(path):
    buggy = []
    with open(path) as f:
        for line in f:
            buggy.append(line.strip().replace(":","."))
    return buggy

def update_ranking_by_category_number(cate_number_dict, bug, method_category_number, method_value, method_final_category):
    best_bug_category_number = method_category_number[bug]
    bug_sus = str(method_value[bug])
    best_bug_category = method_final_category[bug]
    method_category_list = np.sort(np.array(cate_number_dict[best_bug_category + "+" + bug]))

    if best_bug_category_number in method_category_list:
        offset = list(method_category_list).count(best_bug_category_number)
    else:
        offset =  0
    return offset

def get_final_ranking(buggy_methods, method_final_category, method_value, cate_number_dict, method_final_category_index, accumulated_method_count):
    global enableUnidebugPlusPlus
    rankings = []
    rankings_dict = defaultdict(dict)
# --- construct rankings structure (sorted by category > sus > plurality) --- #
    for methodName in sorted(method_value.keys()):
        bug = methodName
        
        bug_cat = method_final_category[bug]
        bug_cat_index = method_final_category_index[bug]
        bug_sus = float(method_value[bug])
 
        #if int(bug_cat_index) != category_indices.index("NoneFix"): # Only look at these type of categorizations
            #continue
        #print(cat_key)

        if(enableUnidebugPlusPlus == "True"):
            plurality_rank = cate_number_dict[bug_cat + "+" + bug][0]
        elif(enableUnidebugPlusPlus == "Star"):
           plurality_rank = accumulated_method_count[methodName]
        else:
            plurality_rank = 0

        if not bug_sus in rankings_dict[bug_cat_index].keys():
            rankings_dict[bug_cat_index][bug_sus] = defaultdict(list)
        rankings_dict[bug_cat_index][bug_sus][plurality_rank].append(bug)

# --- determine each method's rank --- #
    bug_rank = 0
    for cat_key in sorted(rankings_dict.keys()):
        for sus_key in sorted(rankings_dict[cat_key].keys(), reverse=True):
            for plurality_key in sorted(rankings_dict[cat_key][sus_key].keys(), reverse=True):
                bug_rank = bug_rank + len(rankings_dict[cat_key][sus_key][plurality_key]) # WORST-CASE
                for method_key in sorted(rankings_dict[cat_key][sus_key][plurality_key]):
                    if method_key in buggy_methods:
                       rankings.append(str(bug_rank))
                #bug_rank = bug_rank + len(rankings_dict[cat_key][sus_key][plurality_key]) # BEST-CASE
    return rankings, rankings_dict

# get the dict: (category + susvalue):[1,2,3,4] "1,2,3,4" represent the number
# of tools with same category as buggy method
# For example, buggy-method-1 will have 3 tools assigning nonfix to it,
# 2 represents that for another method-2 (also nonefix) has 2 tools assinging
# nonefix to method-2
# And buggy-method-1 and method-2 has the same susvalue
def get_category_number_info(buggy_methods, method_final_category, method_value, method_category_number):
    cate_meth_dict = defaultdict(set)   # value:set(meth1,meth2,meth3...)
    cate_number_dict = defaultdict(list)

    for buggy_m in sorted(method_value):  # All bugs
        buggy_value = method_value[buggy_m]            
        buggy_cat = method_final_category[buggy_m]

        cat_and_value = buggy_cat + "+" + buggy_m

        cate_meth_dict[cat_and_value].add(buggy_m)
        mtd_list = cate_meth_dict[cat_and_value]

        for mtd in mtd_list:
            cate_number_dict[cat_and_value].append(method_category_number[mtd]) 
    return cate_number_dict

def read_comb(comb_file):
    co_list = []
    with open(comb_file) as f:
        for line in f:
            co_list.append(line.strip())
    return co_list

def write_results(result_list,comb_file,comb,max_top1):
    global first_write
    if(first_write is False):
        with open("result." + comb_file,'w') as f:
            first_write = True
            f.write("<Format = Top1 Top3 Top5 MFR MAR from Tool(s)>")
            f.write("\n")

    with open("result." + comb_file,'a') as f:
        if int(result_list[0]) > max_top1:    
            value = int(result_list[0])
            print("\t- Best Top1 found! (previous max vs now)", str(max_top1), value)
            max_top1 = value
       
        f.write(" ".join(
        [
        "{:d}".format(result_list[0]),
        "{:d}".format(result_list[1]),
        "{:d}".format(result_list[2]),
        "{:d}".format(result_list[3]),
        "{:d}".format(result_list[4]),
        "{:d}".format(result_list[5]),
        "{:3.06f}".format(result_list[6]),
        "{:3.06f}".format(result_list[7]),
         ]))
 
        if(comb == ""):
            comb = "SBFL"
        f.write(" from " + comb)
        f.write("\n")
    return max_top1

def get_SBFL_ranking(file):
    buggy_SBFL_ranking = dict()

    if os.path.exists(file):
        with open(file) as f:
            for line in f:
                m = line.split()[0].replace(":",".")

                ranking = line.split()[1].strip()
                buggy_SBFL_ranking[m] = ranking

    return buggy_SBFL_ranking

def outputAggregated(all_methods_rank, proj, ver, variant, combinations, category_indices, buggy_methods):
    if combinations == "":
        combinations = "_SBFL"

    tool_path = "-".join(combinations.split(" "))
    output_dir = "/".join(["manual-review", tool_path, proj + "-" + str(ver), variant])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    f = open("/".join([output_dir, "aggregatedSusInfo.profl"]), "w")
    
    bug_rank = 0
    for cat_key in sorted(all_methods_rank.keys()):
        for sus_key in sorted(all_methods_rank[cat_key].keys(), reverse=True):
            for plurality_key in sorted(all_methods_rank[cat_key][sus_key].keys(), reverse=True):
                bug_rank = bug_rank + len(all_methods_rank[cat_key][sus_key][plurality_key]) # WORST-CASE

                for method_key in sorted(all_methods_rank[cat_key][sus_key][plurality_key]):
                    message = "|".join(["{:04d}".format(bug_rank), "{:06f}".format(sus_key), "PatchCategory." + category_indices[cat_key], "{:010d}".format(plurality_key), method_key])

                    if method_key in buggy_methods:
                        message = "***" + message + "***"

                        if int(bug_rank) <= 1:
                           message = "{} RankTop-1".format(message)
                        if int(bug_rank) <= 3:
                           message = "{} RankTop-3".format(message)
                        if int(bug_rank) <= 5:
                           message = "{} RankTop-5".format(message)

                    f.write(message)
                    f.write("\n")
                #bug_rank = bug_rank + len(all_methods_rank[cat_key][sus_key][plurality_key]) # BEST-CASE


# ------------ Beginning of actual script ------------#
first_write = False

cachedGeneralSus = dict()
cachedAggregatedSus = dict()
cachedMethodCount = dict()

single_tool_base_path = "../../Results/IntermediateResults/profl-unmodified-5th-mixed/worst-case/" # TSE-DATA

comb_file = sys.argv[1] #what tools for aggregation: for example, "SimFix PraPR FixMiner"
unmodified_category = sys.argv[2]  #four mixed options: "CleanFix","NoisyFix","NoneFix","NegFix"
enableUnidebugPlusPlus = sys.argv[3]
sbfl_formula = sys.argv[4]   # formula such as: "STOchiai"
profl_variant = sys.argv[5]
statement_level = sys.argv[6]
pickProjects = 0

if len(sys.argv) >= 8:
    pickProjects = sys.argv[7]

projects = ["Lang","Time","Math","Chart"]
vers = [65,27,106,26]

if pickProjects == "1":
    projects = ["Lang","Time","Math","Chart","Mockito","Closure"]
    vers = [65,27,106,26,38,133]
elif pickProjects == "2":
    projects = ["Mockito","Closure"]
    vers = [38,133]
elif pickProjects == "3":
    projects = ["Mockito"]
    vers = [38]
elif pickProjects == "4":
    projects = ["Closure"]
    vers = [133]

result_list = [["" for x in range(0, vers[y])] for y in range(0, len(projects))]  #initialilize final results

category_indices = ["CleanFixFull", "CleanFixPartial", "CleanFix", "NoisyFixFull", "NoisyFixPartial", "NoisyFix", "NoneFix", "NegFix", "Unmodified"]

tool_combinations = read_comb(comb_file)

max_top1 = 0
index = 0

for comb in tool_combinations:
    if comb.startswith("#"): # Provide way for clean data separation
        print("---", comb[1:].strip() ,"---")
    elif comb.startswith("!"): # Skip line
        pass
    else:    
        tool_combs = comb.split()
        for current_iteration_number in range(0, len(projects)): # Each project
            proj = projects[current_iteration_number]
            vs = vers[current_iteration_number]
    
            for ver in range(1, vs + 1):
                    ver = str(ver)
                    if statement_level == "Method":
                        buggy_method_path = "../../Data/FaultyMethods/" + proj + "/" + ver + ".txt"
                        buggy_methods = get_buggy(buggy_method_path)
                    else:
                        buggy_stmt_path = "../../Data/StatementLevel/buglines/" + proj + "/" + ver + ".txt"
                        buggy_methods = get_buggy_statment(buggy_stmt_path)
    
                    if statement_level == "Method": # Method-level
                        buggy_SBFL_ranking = get_SBFL_ranking("../../Results/SBFLRelated/MBFLBugRanks/" + sbfl_formula + "/" + proj + "-" + ver + ".txt")
                        SusValues = get_current_SBFL_value("../../Results/SBFLRelated/MBFLSusValues/" + sbfl_formula + "/" + proj + "-" + ver + ".txt")
                    else: # Statement-level
                        buggy_SBFL_ranking = get_SBFL_ranking("../../Data/StatementLevel/BugRanks/" + proj + "-" + ver + ".txt") # default Ochiai
                        SusValues = get_current_SBFL_value("../../Data/StatementLevel/st_results/" + proj + "/" + ver + "-s.csv")
    
    		# method value = dict of method suspicious values
    		# method_category = index variant describing all the categories assigned to a tool
    		# method_all_category = describes all categories assigned per method
                    method_category, method_value, method_all_category, accumulated_method_count = get_basic(tool_combs, single_tool_base_path, proj, ver, unmodified_category, SusValues, sbfl_formula, profl_variant, statement_level)
                    # print(method_all_category)
    		# method_final_category = describes best category per method
    		# method_final_category_index = describes index of best category per method
    		# method_category_number = describes the number of tools which assign each method's best category
                    method_final_category, method_category_number, method_final_category_index = get_method_info(method_category, method_value, method_all_category, ver, proj, sbfl_formula)
     
                    cate_number_dict = get_category_number_info(buggy_methods, method_final_category, method_value, method_category_number)
    
                    # buggy_methods_rank = describes the ranks of specific buggy methods
                    # all_methods_rank = describes all the information needed to accurately detrmine the rank of all methods
                    buggy_methods_rank, all_methods_rank = get_final_ranking(buggy_methods, method_final_category, method_value, cate_number_dict, method_final_category_index, accumulated_method_count)
                    buggy_methods_rank_string = ",".join(buggy_methods_rank)
             
                    result_list[current_iteration_number][int(ver) - 1] = buggy_methods_rank_string
    		
                    if True:
                        outputAggregated(all_methods_rank, proj, ver, profl_variant, comb, category_indices, buggy_methods)
    
        final_result, true_ver = ut.get_static_final(vers, projects, result_list) # get top-1,3,5...  for each projects
        final_result = ut.get_final(final_result, true_ver) # get final result
    
        print("Combination", index, "metric results =", final_result) 
        max_top1 = write_results(final_result, comb_file, comb, max_top1)
    index = index + 1

print("-----------------------")
print("Best Top-1 results were", max_top1)
