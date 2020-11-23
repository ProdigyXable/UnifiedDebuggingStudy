##Get 16*33 features

import os.path
import os
from collections import defaultdict
import numpy as np

value_set = set()
def get_value(file):
	value_dict = dict()
	if os.path.exists(file):
		with open(file) as f:
			for line in f:
				method = line.split(" ")[0]
				value = line.split(" ")[1].strip()
				value_dict[method] = value
				if abs(float(value)) > 0:
					value_set.add(abs(float(value)))
	return value_dict,value_set
def write_data(final_dict,file):
	with open(file,'a') as f:
		for m in final_dict:
			values = final_dict[m]
			f.write(m + " ")
			s = ",".join(values) 
			f.write(s)
			f.write("\n")
def get_category(file,sus_dict):
	category_dict = dict()
	if not os.path.exists(file):
		for method in sus_dict:
			category_dict[method] = 0
			#print(file)
	else:
		with open(file) as f:
			for line in f:
				line = line.strip()
				method = line.split("|")[3]
				category = line.split("|")[2].split("PatchCategory.")[1]
				cat = category_replace[category]
				category_dict[method] = cat
	for m in sus_dict:
		if m not in category_dict:
			category_dict[m] = 0
	return category_dict



sus_path = "../../../Data/DeepFLData/SusValue/"   #path of sus values of 33 sbfl 
cate_path = "../../../Data/ExperimentalData/"  #path of category of each method




projects = {"Chart":26,"Time":27,"Lang":65,"Math":106,"Mockito":38,"Closure":133}
#projects = {"Chart":1}
category_replace = {"CleanFix":7000000,"NoisyFix":5000000,"NoneFix":3000000,"NegFix":1000000,"Unmodified":1000000}


#sbfl_formula = ["STAmple","STAnderberg","STDice","STDStar2","STER1a","STER1b","STER5c","STEuclid","STGoodman","STGP02","STGP03","STGP13","STGP19",
#				"STHamann","STHamming","STJaccard","STKulczynski1","STKulczynski2","STM1","STM2","STOchiai","STOchiai2","STOverlap","STrensenDice",
#				"STRogersTanimoto","STRussellRao","STSBI","STSimpleMatching","STSokal","STTarantula","STWong","STWong3","STZoltar"]
sbfl_formula = ["STOchiai"]
repair_tools = ["ProFL-ACS","ProFL-Arja","ProFL-AvatarFixer","ProFL-Cardumen","ProFL-Dynamoth","ProFL-FixMiner","ProFL-GenProgA","ProFL-jGenProg",
				"ProFL-jKali","ProFL-jMutRepair", "ProFL-KaliA","ProFL-kParFixer","ProFL-PraPR","ProFL-RSRepair","ProFL-Simfix","ProFL-TBarFixer"]

#repair_tools = ["ProFL-ACS","ProFL-AvatarFixer","ProFL-Cardumen","ProFL-Dynamoth","ProFL-FixMiner","ProFL-jGenProg",
#				"ProFL-jKali","ProFL-jMutRepair", "ProFL-KaliA","ProFL-kParFixer","ProFL-PraPR","ProFL-Simfix","ProFL-TBarFixer"]

repair_tools = ["ProFL-ACS"]



for pro in projects:
	versions = projects[pro]
	for ver in range(0,versions):
		ver = str(ver + 1)
		final_dict = defaultdict(list)   #13*33 features  
		#for single_tool in repair_tools:
		for formula in sbfl_formula:
			sus_dict,valus_list = get_value(sus_path + formula + "/" + ver + "-" + pro + ".txt")
			'''
				cate_dict = get_category(cate_path + single_tool + "/" + pro + "-" + ver + "/aggregatedSusInfo.profl",sus_dict)
				for method in sus_dict:
					sus_v = sus_dict[method]
					#if method in cate_dict:
					cate = cate_dict[method]						
					new_value = float(sus_v) + float(cate) 
					final_dict[method.replace(":",".")].append(str(new_value))
		for m in final_dict:
			if len(final_dict[m]) != 429:
				print(pro + " " + ver + " ERROR")
		'''	
		#write_data(final_dict,"../../Data/DeepFLData/AllToolNewFeatures/" + pro + "/" + ver + ".txt")
value_list = np.array(list(value_set))
print(np.amax(value_list))
print(np.amin(value_list))

