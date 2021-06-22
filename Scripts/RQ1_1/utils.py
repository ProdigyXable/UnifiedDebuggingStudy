import numpy as np
def parse_res(res):
    min = -1
    avg = -1
    if res != "":
        if "," not in res:
            min = int(res)
            avg = int(res)
        else:
            all = np.array([int(r) for r in res.split(",")])
            min = np.min(all)
            avg = np.mean(all)
    return min,avg

def get_static_final(projects, ver, result_list):
    
    final_result = []
    true_ver = []
    venn_result = []
    
    for index in range(0,len(projects)):   #each project
        results_by_proj = result_list[index]

        tops = np.zeros(6)
        ranks = np.zeros(2)
        ranks_min = list()  #first
        ranks_avg = list()  #all
        actual_ver = 0
        for res in results_by_proj:   #result of each version
            if res == "":
                venn_result.append(0)
            else:
                min,avg = parse_res(res)
                if min == 1:
                    venn_result.append(1)
                else:
                    venn_result.append(0)

                if min <= -1:
                    print("Rank is below 0 / -1")
                    continue
                if min <= 1: # Top-1
                    tops[0] += 1
                if min <= 3: # Top-3
                    tops[1] += 1
                if min <= 5: # Top-5
                    tops[2] += 1
                if min <= 10: # Top-10
                    tops[3] += 1
                if min <= 25: # Top-25
                    tops[4] += 1
                if min <= 50: # Top-50
                    tops[5] += 1

                ranks[0] += min
                ranks[1] += avg

                ranks_min.append(min)
                ranks_avg.append(avg)
                actual_ver += 1
        true_ver.append(actual_ver)
        if actual_ver == 0:
            ranks = [0,0]
        else:
            ranks = ranks / actual_ver 

        result = (int(tops[0]), int(tops[1]), int(tops[2]), int(tops[3]), int(tops[4]), int(tops[5]), float(ranks[0]), float(ranks[1]))
        result = np.array(result, dtype=object)

        final_result.append(result)
    final_result = np.array(final_result)
    return final_result,true_ver

def get_final(final_result,true_ver):
    np_topn = final_result[:,0:6]
    np_mean = final_result[:,6:8]
    np_top = np.sum(np_topn,0)
    np_mean = np_mean * np.transpose(true_ver).reshape(len(true_ver),1)
    np_mean = np.sum(np_mean,0)/max(1, np.sum(true_ver))
    final_result = np.concatenate((np_top,np_mean))
    return final_result
