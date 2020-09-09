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

def get_all_versions():
	projects = ["Lang","Time","Math","Chart"]
	ver = [65,27,106,26]
	all_versions = []
	for index in range(0,len(projects)):
		vs = ver[index]
		for v in range(1,vs + 1):
			all_versions.append(projects[index] + "-" + str(v))
	return all_versions

all_versions = get_all_versions()

correct_dic = get_info("correct.txt")

for tool in correct_dic:
	correct_ver_list = correct_dic[tool]
	with open("AllIncorrect.txt",'a') as f:
		f.write(tool + ":")
		for v in all_versions:
			if v not in correct_ver_list:
				f.write(v + " ")
		f.write("\n")


