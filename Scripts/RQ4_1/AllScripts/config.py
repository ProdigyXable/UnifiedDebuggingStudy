import sys

single_tool_base_path = "../../../Data/ExperimentalData/ProFL-"

projects = ["Lang","Time","Math","Chart","Mockito","Closure"]
vers = [65,27,106,26,38,133]

#projects = ["Lang","Time","Math","Chart"]
#vers = [65,27,106,26]

#projects = ["Lang"]
#vers = [1]

#projects = ["Mockito","Closure"]
#vers = [38,133]


comb_file = sys.argv[1] #what tools for aggregation: for example, "SimFix PraPR FixMiner"
sbfl_formula = sys.argv[2]   # formula such as: "STOchiai"
mix_unmodified = sys.argv[3]  #four mixed options: "CleanFix","NoisyFix","NoneFix","NegFix"
unidebug_variant = sys.argv[4]  # 1+2, 1+2+3...

#if(len(sys.argv) > 3):
#    unidebug_plusplus = sys.argv[3]

unmodified_ranking = ["CleanFix","NoisyFix","NoneFix","NegFix"]
unmodified_ranking_replace = [7000000,5000000,3000000,1000000]