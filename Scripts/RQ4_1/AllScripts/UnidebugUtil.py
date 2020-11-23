import os
from config import *
from collections import defaultdict
import numpy as np
from decimal import Decimal
def read_comb(comb_file):
    co_list = []
    with open(comb_file) as f:
        for line in f:
            co_list.append(line.strip())
    return co_list
def get_buggy(buggy_method_path):
    buggy = []
    with open(buggy_method_path) as f:
        for line in f:
            if  "^^^^^^" in line:
                buggy.append(line.split("^^^^^^")[1].strip().replace(":","."))
    return buggy
def get_SBFL_ranking(file, buggy_methods):
    buggy_SBFL_ranking = dict()
    if os.path.exists(file):
        with open(file) as f:
            for line in f:
                m = line.split("  ")[0].replace(":",".")
                ranking = line.split("  ")[1].strip()
                buggy_SBFL_ranking[m] = ranking

    return buggy_SBFL_ranking
def get_current_SBFL_value(file):
    sus_dic = dict() 
    if os.path.exists(file):   
        with open(file) as f:
            for line in f:
                method_name = line.split()[0].replace(":",".")
                value = line.split()[1].strip()
                sus_dic[method_name] = value
    return sus_dic

def get_category_list(tool_combs,single_tool_base_path,proj,ver,mix_unmodified,sbfl_formula):
    method_categories = defaultdict(list) #index of Unmodified_ranking
    for tool in tool_combs:
        if not os.path.exists(single_tool_base_path + tool):
            print(single_tool_base_path + tool + "DOES NOT EXISIT!")
        result_file = single_tool_base_path + tool + "/" + proj + "-" + ver + "/aggregatedSusInfo.profl"

        if os.path.exists(result_file):
            with open(result_file) as f:
                for line in f:
                    items = line.strip().split("|")
                    method_name = items[3].replace(":",".")
                    category = items[2].split("PatchCategory.")[1]
                    if category == "Unmodified":
                        category = mix_unmodified
                    method_categories[method_name].append(unmodified_ranking.index(category))  # Method-1:[0,1,2,2,..]


                       #store_cate_each_tool(method_name,cate, "/home/xia/T/TSEUniDebug/UnifiedDebuggingStudy67a46b0/Data/BaseData/CategoryEachTool/" + tool )

                        #folder = "../../Data/DeepFLData/SusValue/" + sbfl_formula
                        #if not os.path.exists(folder):
                        #    os.makedirs(folder)                              
                        #write_data(method_name,value,folder + "/" + ver + "-" + proj + ".txt")
    return method_categories

#method_final_category: method with final category, used for single tool and unidebug+
#method_category_number: method with repair tool number with best final category, used for unidebug++
def get_final_category(method_categories,ver,proj,sbfl_formula):
    method_final_category = dict()   # final category
    method_category_number = dict() # number of cleanfix/Noisyfix/NoneFix for all tools
    for m in method_categories:
        category_list = method_categories[m]
        min_number = np.array(category_list).min()
        method_final_category[m] = min_number        
        category_number = category_list.count(min_number)
        if category_number > 0:
            method_category_number[m] = category_number
            

            '''
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
            '''
    return method_final_category,method_category_number
def pre_ranking(SBFL_sus_values,method_final_category,method_category_number,patch_number_dict):
    final_values_dict = dict()
    final_values_list = []
    for method in SBFL_sus_values:
        if method in method_final_category:
            category_v = Decimal(unmodified_ranking_replace[method_final_category[method]])   # 1
            SBFL_v = Decimal(SBFL_sus_values[method])     # 2        
            tool_number_v = Decimal(method_category_number[method]/100000000000)   #3
            patch_number_v = Decimal(patch_number_dict[method][method_final_category[method]]/100000000000) #4
            if unidebug_variant == "1+2+4":
                final_value = SBFL_v + category_v + patch_number_v
            elif unidebug_variant == "1+2+3":
                final_value = SBFL_v + category_v + tool_number_v     # original unidebug++
            elif unidebug_variant == "1+2":
                final_value = SBFL_v + category_v # original Profl and unidebug+
            final_values_dict[method] = final_value
            final_values_list.append(final_value)
    return final_values_dict,final_values_list

def ranking(final_values_dict,final_values_list,buggy_methods,buggy_SBFL_ranking):
    rankings = []
    final_values_list.sort()
    #print(final_values_list)
    for bug in buggy_methods:
        if bug in final_values_dict:
            value = final_values_dict[bug]
            ranking = len(final_values_list) - final_values_list.index(value) 
            rankings.append(str(ranking))
        else:
            if bug in buggy_SBFL_ranking:
                rankings.append(buggy_SBFL_ranking[bug])
    return rankings


def get_all_methods(file):
    all_methods = list()
    if os.path.exists(file):
        with open(file) as f:
            for line in f:
                all_methods.append(line.strip().split()[0].replace(":","."))
    return all_methods

def get_all_patch_number(tool_comb,proj,ver):
    all_methods = get_all_methods("../../../Results/SBFLRelated/SBFLSusValues/STOchiai/" + proj + "-" + str(ver) + ".txt")
    final_dict = dict()
    for tool in tool_comb:
        count_file = "../../../Data/PatchCountData/ProFL-" + tool + "/" + proj + "-" + str(ver) + "/proflvariant-full-standard/category_information.profl"
        if os.path.exists(count_file):
            with open(count_file) as f:
                for line in f:
                    line = line.strip()
                    if ":" in line:
                        method = line.split(" = ")[0].replace(":",".")
                        patch_count_each_tool = [[0 for x in range(0,len(unmodified_ranking))] for y in range(0,len(tool_comb))]
                        final_dict[method] = np.array(patch_count_each_tool)


    for tool in tool_comb:
        count_file = "../../../Data/PatchCountData/ProFL-" + tool + "/" + proj + "-" + str(ver) + "/proflvariant-full-standard/category_information.profl"
        if os.path.exists(count_file):
            with open(count_file) as f:
                category_flag = ""
                for line in f:
                    line = line.strip()
                    if line.startswith("=== Number of PatchCategory."):
                        category_flag = line.split("=== Number of PatchCategory.")[1].split(" = ")[0]
                        #print(category_flag)
                    if category_flag != "" and ":" in line:
                        method = line.split(" = ")[0].replace(":",".")
                        count = line.split(" = ")[1].strip()
                        
                        final_dict[method][tool_comb.index(tool)][unmodified_ranking.index(category_flag)] = int(count)
                        #final_dict[method] = new_matrix
    count_dict = dict()
    for m in final_dict:
        counts = final_dict[m]
        new_m = m.replace(":",".")
        counts = np.sum(counts, axis=0)
        count_dict[new_m] = counts
    for m in all_methods:
        if m not in count_dict:
            count_dict[m] = [0,0,0,len(tool_comb)]
    return count_dict




