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
correct_dic = get_info("correct.txt")

for tool in plau_dic:
	if tool not in correct_dic:
		print(tool + " not in correct file!!!!")
	else:
		print(tool)
		plau_ver_list = plau_dic[tool]
		correct_ver_list = correct_dic[tool]
		with open("incorrectButPlau.txt",'a') as f:
			f.write(tool + ":")
			for v in plau_ver_list:
				if v not in correct_ver_list:
					f.write(v + " ")
			f.write("\n")


