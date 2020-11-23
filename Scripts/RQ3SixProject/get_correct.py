# Intersection of correctFromPaper and plausible


from collections import defaultdict

def get_info(path):
	ver_dic = defaultdict(list)
	with open(path) as f:
		for line in f:
			if ":" in line:
				tool = line.split(":")[0]
				versions = line.strip().split(":")[1].split()
				ver_dic[tool] = versions
	return ver_dic


plau_dic = get_info("plausible.txt")
correct_dic = get_info("correctFromPaper.txt")

for tool in plau_dic:
	if tool not in correct_dic:
		print(tool + " not in correct file!!!!")
	else:
		plau_ver_list = plau_dic[tool]
		correct_ver_list = correct_dic[tool]
		new_correct_list = set(plau_ver_list).intersection(set(correct_ver_list))
		new_correct_list = list(new_correct_list)
		with open("correct.txt",'a') as f:
			f.write(tool + ":")
			for v in new_correct_list:
				f.write(v + " ")
			f.write("\n")

