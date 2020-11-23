import os.path
import os
from collections import defaultdict
def get_value(file):
	value_dict = dict()
	if os.path.exists(file):
		with open(file) as f:
			for line in f:
				method = line.split(" ")[0]
				value = line.split(" ")[1].strip()
				if value in category_replace:
					value = category_replace[value]
				value_dict[method] = value
	return value_dict
def write_data(final_dict,file):
	with open(file,'a') as f:
		for m in final_dict:
			values = final_dict[m]
			f.write(m + " ")
			s = ",".join(values) 
			f.write(s)
			f.write("\n")



sus_path = "../../Data/DeepFLData/SusValue/"
cate_path = "../../Data/DeepFLData/Category/"
cate_number_path = "../../Data/DeepFLData/CategoryNumber/"



projects = {"Chart":26,"Time":27,"Lang":65,"Math":106,"Mockito":38,"Closure":133}

category_replace = {"CleanFix":400,"NoisyFix":300,"NoneFix":200,"NegFix":100}


sbfl_formula = ["STAmple","STAnderberg","STDice","STDStar2","STER1a","STER1b","STER5c","STEuclid","STGoodman","STGP02","STGP03","STGP13","STGP19",
				"STHamann","STHamming","STJaccard","STKulczynski1","STKulczynski2","STM1","STM2","STOchiai","STOchiai2","STOverlap","STrensenDice",
				"STRogersTanimoto","STRussellRao","STSBI","STSimpleMatching","STSokal","STTarantula","STWong","STWong3","STZoltar"]


for pro in projects:
	versions = projects[pro]
	for ver in range(0,versions):
		ver = str(ver + 1)
		final_dict = defaultdict(list)
		for formula in sbfl_formula:
			sus_dict = get_value(sus_path + formula + "/" + ver + "-" + pro + ".txt")
			cate_dict = get_value(cate_path + formula + "/" + ver + "-" + pro + ".txt")
			cate_num_dict = get_value(cate_number_path + formula + "/" + ver + "-" + pro + ".txt")
			for method in sus_dict:
				sus_v = sus_dict[method]
				if method in cate_dict and method in cate_num_dict:
					cate = cate_dict[method]
					cate_number = cate_num_dict[method]
					new_value = float(sus_v) + float(cate) + float(cate_number)
					final_dict[method.replace(":",".")].append(str(new_value))
		write_data(final_dict,"../../Data/DeepFLData/NewFeatureUniDebug/" + pro + "/" + ver + ".txt")
			

