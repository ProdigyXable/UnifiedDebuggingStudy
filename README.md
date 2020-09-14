## On the Effectiveness of Unified Debugging: An Extensive Study on 16 Program Repair Systems ##
 
This repository contains the dataset and scripts for *On the Effectiveness of Unified Debugging: An Extensive Study on 16 Program Repair Systems* - Automated Software Engineering (ASE'20).

## 1.  Content ##

### 1.1 [Data](Data/) ###

- **[ExperimentalData](Data/ExperimentalData/)**: the raw experimental dataset.
    -  **ProFL-\[*toolName*]/\[*d4j-project*]/**: data for each APR tool on each project.
	    - **generalSusInfo.profl**: spectrum-based fault localization based on Ochiai and aggregation strategy.  (Methods with zero suspiciousness are excluded and tied methods all  receive *worse rank*).
		``` 
		[MethodRank 1] | [Suspiciousness Score 1] | [MethodSignature 1]; 
		[MethodRank 2] | [Suspiciousness Score 2] | [MethodSignature 2];
    	...
    	[MethodRank N] | [Suspiciousness Score N] | [MethodSignature N];
    	```

		- **aggregatedSusInfo.profl**: unfied debugging fault localization.  Patch caregory (i.e., *CleanFix*, *NoisyFix*, *NoneFix*, *NegFix*, or Unmodified) refers to the highest priority patch category associated with each method. 
		```
    [MethodRank 1] | [Suspiciousness Score 1] | Patch Category 1 | [MethodSignature 1];
    [MethodRank 2] | [Suspiciousness Score 2] | Patch Category 2 | [MethodSignature 2];
    ...
    [MethodRank N] | [Suspiciousness Score N] | Patch Category N | [MethodSignature N];
    ```
-  **[FaultyMethods](Data/FaultyMethods/)**: ground truth of faulty methods.



### 1.2 [Scripts](Scripts/) ###
Include scripts to reproduce results, table, and figures in the paper.


- **RQ1_1**: Contains data and script to generate the table corresponding to Figure 3.
- **RQ1_2**: Contains the data and script to generate Figure 7.
- **RQ2**: Contains the data and script to generate Figure 8.
- **RQ3**: Contains the data and script to generate Figure 9.
- **RQ4_1**: Contains the script to generate the result of UniDebug+ and UniDebug++.
- **RQ4_2**: Contains the data and script to generate Figure 10.
- **RunFinalResult.sh**: an All-In-One script to run other scripts. Described in Section 2.

### 1.3 [Results](Results/) ###

The structure of this folder is as follows.
 
 - **FinalResults**: Final results generated from the [scripts](Scripts/) folder.
 - **IntermediateResults**: Intermidiate results used to generate final results.
 - **SBFLResults**: Ground truth results from spectrum-based fault localization.


## 2. Reproduce Tables & Figures ##

### 2.1  Requirements ###
 To run this repository plesee ensure your enviroment satisfy the following requirements.
 - Python 3
 - R (Package "ggpubr", "ggplot2", "reshape2", "cowplot" are required)

### 2.2 Commands ###
To recreate the paper's tables and figures, run the following command:

```
cd Scripts
bash RunFinalResult.sh $RQ
```
$RQ represents a research question and the results will be generated in [Results/FinalResults](Results/FinalResults). (*Note See RQ4_1 for specific configurable parameters for RQ4_1. Running RQ4_1 will output UniDebug++ results from Table 5.*) Output for different arguments of $RQ:

- RQ1_1: RQ1_1.csv, corresponding to Figure 3.
- RQ1_2: RQ1_2.pdf, corresponding to Figure 7.
- RQ2: RQ2.pdf, corresponding to Figure 8.
- RQ3: RQ3_*.pdf, corresponding to Figure 9.
- RQ4_1: *.result files, corresponding to the specific combination of tools. Output generated in RQ4_1 instead of Results/FinalResults. 
- RQ4_2: RQ4_2.pdf, corresponding to Figure 10.

### 2.3 Configuring RQ4_1 ###

Table 5's results can be reproduced with the main script [AggreCombinePatch.py](Scripts/RQ4_1/AggreCombinePatch.py), generating the results of UniDebug+ and UniDebug++.

This file can be executed with the following command:

``` python
python AggreCombinePatch.py <Tool Combination File> [CleanFix | NoisyFix | NoneFix | NegFix]
```
After running such a command, a \*.result file will be generated in [Scripts/RQ4_1](Scripts/RQ4_1), describing the metrics for each combination.

The ***Tool Combination File*** is a file containing a line delimited list of attempted project combinations.
A list of available names can be found in [IndividualCombinations.txt](Scripts/RQ4_1/IndividualCombinations.txt).
The supplied Tool Combination File should be located within the [Scripts/RQ4_1/](Scripts/RQ4_1/) directory.

The script's second argument represents which patch category Non-Modify code elements (methods which are unmodified by a repair tool) fall into.

Running the following command will reflect the UniDebug++ results in the ASE'20 paper and generate a ***GreedyTop1.txt.result*** file in [Scripts/RQ4_1/](Scripts/RQ4_1/).

``` python
python AggreCombinePatch.py GreedyTop1.txt NegFix
```
If you wish to obtain UniDebug+ results, instead of UniDebug++, you may provde a third argument as follows:

``` python
python AggreCombinePatch.py GreedyTop1.txt NegFix False
```

Running the following command will exhaustively attempt all combinations of the 16 repair tools and generate a ***ExhaustiveCombinations.txt.result*** file in [Scripts/RQ4_1/](Scripts/RQ4_1/), reflecting the UniDebug++ technique.

``` python
python AggreCombinePatch.py ExhaustiveCombinations.txt NegFix
```

\*\**Note that each successful run of AggreCombinePatch.py ***appends*** data to any existing file. Thus, you may wish to clear or move the results after every run*

## 3. Additional Information ##
For additional information, such as tables / figures, view the project wiki.


