#!/bin/sh
RQ=$1

if [ $RQ = "RQ1_1" ]
 then
  rm -rf ../Results/FinalResults/RQ1_1.csv
  tools="jGenProg genprogA jMutRepair kPar rsrepair jKali kaliA dynamoth acs cardumen arja simfix fixMiner avatar tbar prapr"
  cd RQ1_1
  for tool in $tools
    do
      python3 ResultAnalysis.py profl-$tool-results_ 4th All
    done
fi

if [ $RQ = "RQ1_2" ]
  then
   rm -rf ../Results/FinalResults/RQ1_2.pdf
   rm -rf ./RQ1_2/Rdata/*.txt
   cd RQ1_2
   python3 RData.py
   Rscript RCode.r
fi


if [ $RQ = "RQ2" ]
  then
   rm -rf ../Results/FinalResults/RQ2.pdf
   cd RQ2
   Rscript rCode.r
fi



if [ $RQ = "RQ3" ]
  then
   rm -rf ../Results/FinalResults/RQ3*
   cd RQ3
   Rscript rCode.r
fi

if [ $RQ = "RQ4_1" ]
  then
   cd RQ4_1
   python3 AggreCombinePatch.py GreedyTop1.txt NegFix
fi


if [ $RQ = "RQ4_2" ]
  then
   rm -rf ../Results/FinalResults/RQ4*
   cd RQ4_2
   Rscript RCode.r
fi
