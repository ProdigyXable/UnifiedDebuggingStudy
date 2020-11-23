from collections import defaultdict

tool_vs = dict()

with open("plausible.txt") as f:
	for line in f:
		if ":" in line:
			tool  = line.split(":")[0]
			versions = line.split(":")[1].split()
			tool_vs[tool] = versions
tool_exclu_versions = defaultdict(list)
for tool_target in tool_vs:    # each target tool
	target_vers = tool_vs[tool_target]   #versions list for target tool
	for target_v in target_vers:         #each version for target tool
		boolean_v = False
		for other_tool in tool_vs:	
			if other_tool != tool_target: #check other tools 
				other_versions = tool_vs[other_tool]
				if target_v in other_versions:
					boolean_v  = True
					break
		if boolean_v == False:
			tool_exclu_versions[tool_target].append(target_v)
for tool in tool_exclu_versions:
	print(tool + " " + str(len(tool_exclu_versions[tool])))