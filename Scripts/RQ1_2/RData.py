


item_names = ["Top1","Top3","Top5","MFR","MAR","TotalPatch","MethodByTotal", "PlausiblePatch","MethodsByPlausible"]

import numpy as np

from collections import defaultdict

full_data = defaultdict(list)
with open("full_results.txt") as f:
	for line in f:
		tool = line.split()[0]

		re = line.strip().split(tool)[1].strip().split()
		full_data[tool.lower()] = re

with open("PatchesAllMethods.txt") as f:
	for line in f:
		tool = line.split()[0]
		if tool in full_data:
			#if tool == "acs":
			#	print(tool)
			patches = line.strip().split(tool)[1].strip().split()
			#if int(patches[0]) < 10000:
			full_data[tool].extend(patches)
final_matrix = []

#del full_data["prapr"]

#for i in full_data:
#	print(i)
#	print(full_data[i])

with open("toolName.txt", "w") as f:
	for tool in full_data:		
		data = full_data[tool]
		if "" not in data:
			f.write(tool + " ")
			if len(data) > 5:
				final_matrix.append(np.array(data))

final_matrix = np.array(final_matrix)

#print(final_matrix)

metric_idx = [0,1,2,3,4]
patch_idx = [5,6,7,8]  #All and Unique

for m in metric_idx:
	for p in patch_idx:
		metric_data = final_matrix[:,m]
		patch_data = final_matrix[:,p]
		file_name = "Rdata/" + item_names[p] + item_names[m] + ".txt"
		with open(file_name,'a') as f:
			for m_data in metric_data:
				f.write(m_data + " ")
			f.write("\n")
			for p_data in patch_data:
				f.write(p_data + " ")
			f.write("\n")

		





