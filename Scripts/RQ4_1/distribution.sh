#!/bin/bash
path=$1
cats=("CleanFix" "NoisyFix" "NoneFix" "NegFix")
ranks=("RankTop-1" "RankTop-3" "RankTop-5")

echo Processing path \"$path\"

tempFile1=$(mktemp)
tempFile2=$(mktemp)

trap "rm ${tempFile1}; rm ${tempFile2}" 0 2 3 15


for rank in ${ranks[@]}
do
	results=()
	lastNum=0
	
	for cat in ${cats[@]}
	do
		data=$(grep -r "${rank}" $path | grep "${cat}" | grep "^.*:" -o | sort -u)

		for d in $data
		do
			echo ${d} >> ${tempFile1}
			sort -u ${tempFile1} > ${tempFile2}
		done

		newLength=$(grep "" ${tempFile2} -c)
		newTopN=$(expr ${newLength} - ${lastNum})
	
		results+=${newTopN}
		results+=" "
		
		lastNum=${newLength}
	done
	echo ${results[@]}
done

