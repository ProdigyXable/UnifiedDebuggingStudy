#!/bin/bash
path=$1
cats=("CleanFix" "NoisyFix" "NoneFix" "NegFix")
ranks=("RankTop-1" "RankTop-3" "RankTop-5")

echo Processing path \"$path\"

for cat in ${cats[@]}
do
	results=()

	for rank in ${ranks[@]}
	do
		data=$(grep -r "${rank}" $path | grep "${cat}" | grep "^.*:" -o | sort -u | wc -l)
        	results+=($data)
	done

	echo $cat ${results[@]}
done

