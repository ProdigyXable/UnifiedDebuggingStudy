import sys
from collections import defaultdict
import numpy as np
import os
sys.path.append("../../RQ1_1/")
import utils as ut
from config import *
import UnidebugUtil as uniutil


def main():    
    combs_from_file = uniutil.read_comb(comb_file)
    max_top1 = 0
    index = 0

    for comb in combs_from_file:
        result_list = [["" for x in range(0,vers[y])] for y in range(0,len(projects))]  #initialilize final results
        tool_combs = comb.split()
        
        for current_iteration_number in range(0,len(projects)):   #each project
            proj = projects[current_iteration_number]
            vs = vers[current_iteration_number]
            for ver in range(1,vs + 1):
                #if proj == "Mockito" and ver == 4:                   
                    ver = str(ver)
                    buggy_methods = uniutil.get_buggy("../../../Data/FaultyMethods/" + proj + "/" + ver + ".txt")                
                    buggy_SBFL_ranking = uniutil.get_SBFL_ranking("../../../Results/SBFLRelated/SBFLBugRanks/" + sbfl_formula + "/" + proj + "-" + ver + ".txt",buggy_methods)
                    SBFL_sus_values = uniutil.get_current_SBFL_value("../../../Results/SBFLRelated/SBFLSusValues/" + sbfl_formula + "/" + proj + "-" + ver + ".txt")                   
                    method_categories = uniutil.get_category_list(tool_combs,single_tool_base_path,proj,ver,mix_unmodified,sbfl_formula)
                    method_final_category,method_category_number = uniutil.get_final_category(method_categories,ver,proj,sbfl_formula)
                    patch_number_dict = uniutil.get_all_patch_number(tool_combs,proj,ver)


                    final_values_dict,final_values_list = uniutil.pre_ranking(SBFL_sus_values,method_final_category,method_category_number,patch_number_dict)
                    final_ranking = uniutil.ranking(final_values_dict,final_values_list,buggy_methods,buggy_SBFL_ranking)           
                    final_r_string = ",".join(final_ranking)
                    result_list[current_iteration_number][int(ver) - 1] = final_r_string

        #print(result_list)
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
      

main()
