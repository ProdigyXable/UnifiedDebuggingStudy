import subprocess
import sys
# grep "NegFix" ProFL-jG*/*/proflvariant-full-extended/cat* -h | grep -v " = 0 ="

project = sys.argv[1]

variant = "proflvariant-full-standard"
patches = ["CleanFix", "NoisyFix", "NoneFix", "NegFix"]

#variant = "proflvariant-full-extended"
#patches = ["CleanFixFull", "CleanFixPartial", "NoisyFixFull", "NoisyFixPartial", "NoneFix", "NegFix"]

for patch in patches:
	command = " ".join(["grep -h", patch, "/".join([project, "*", variant, "cat*"])])
	data = subprocess.check_output(command, shell=True).decode("UTF-8").split("\n")
	acc = 0
	
	for s in data:
		d = s.split("=")
		if(len(d) > 4): 
			acc = acc + int(d[4].strip())
	print(patch, acc)
