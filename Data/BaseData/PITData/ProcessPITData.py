from collections import defaultdict
import numpy as np
import os
projects = ["Lang","Time","Math","Chart","Mockito","Closure"]
vers = [65,27,106,26,38,133]
#projects = ["Chart"]
#vers = [1]
PIT_result_path = "mutatorResults-0"

def get_method_name(file_name):
   method_idx_dic = dict()
   with open(file_name) as f:
      for line in f:
         idx = line.split(",")[0]
         name = line.strip().split(",")[2]
         method_idx_dic[idx] = name
  
   return method_idx_dic
def write_file(method_dict,path,proj,v):
   #os.makedirs(path +"/" + proj + "-" + v)
   with open(path +"/" + proj + "-" + v + "/aggregatedSusInfo.profl",'a') as f:
      for method in method_dict:
         f.write("0|0|PatchCategory." + method_dict[method] + "|" + method)
         f.write("\n")


for current_iteration_number in range(0,len(projects)):   #each project
   proj = projects[current_iteration_number]
   vs = vers[current_iteration_number]
   for ver in range(1,vs + 1):                 
      ver = str(ver)
      method_result_change = defaultdict(list)
      method_file = "MethodInfo/" + proj + "/" + ver + "-methodInfo.csv"
      if os.path.exists(method_file):
         method_idx_dic = get_method_name(method_file)
      file_name = PIT_result_path + "/"+ proj + "/" + ver + "-all.csv"
      if os.path.exists(file_name):
         with open(file_name) as f:
            for line in f:
               items = line.strip().split(",")
               mutator = items[0]
               if mutator.startswith("org.pitest"):
                  method_idx = items[2]
                  if method_idx in method_idx_dic:
                     method_name = method_idx_dic[method_idx]
                     f2p = int(items[4])
                     p2f = int(items[8])
                     change_values = [f2p,p2f]
                     method_result_change[method_name].append(change_values)
         #print(method_result_change)
         final_dict = dict()
         for method in method_result_change:
            changes = method_result_change[method]
            changes = np.array(changes)
            changes_sum = np.sum(changes,axis=0)
            f2p = changes_sum[0]
            p2f = changes_sum[1]
            if f2p > 0 and p2f == 0:
               final_dict[method] = "CleanFix"
            if f2p > 0 and p2f > 0:
               final_dict[method] = "NoisyFix"
            if f2p == 0 and p2f == 0:
               final_dict[method] = "NoneFix"
            if f2p == 0 and p2f > 0:
               final_dict[method] = "NegFix"
         write_file(final_dict,"PITCleanResult/" + "ProFL-PIT",proj, ver)
         




