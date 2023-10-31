from csv import reader
from collections import defaultdict
from itertools import chain, combinations
from optparse import OptionParser
import until

def apriori(data_list, min_sup, minConf):
    c1_item_set = until.ItemSet_FromList(data_list)
    # 最終目標 frequent itemset
    global_FreqItem_Set = dict()
    global_ItemSet_sup = defaultdict(int)

    k = 2
    L1_ItemSet = above_min_sup(c1_item_set, data_list, min_sup, global_ItemSet_sup)
    current_LSet = L1_ItemSet
    

    # 計算 frequent item set
    while(current_LSet):
        # 排序
        global_FreqItem_Set[k-1] = current_LSet
        # Self-joining Lk
        candidate_Set = getUnion(current_LSet, k)
        # 子集測試，剪枝
        candidate_Set = pruning(candidate_Set, current_LSet, k-1)
        # 根據sup遍歷data
        current_LSet = above_min_sup(candidate_Set, data_list, min_sup, global_ItemSet_sup)
        k += 1

    rules = until.associationRule(global_FreqItem_Set, global_ItemSet_sup, minConf)
    rules.sort(key=lambda x: x[2])

    return global_FreqItem_Set, rules

def getUnion(itemSet, length):
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

def pruning(candidate_Set, prevFreqSet, length):
    temp_candidate_Set = candidate_Set.copy()
    for i in candidate_Set:
        subsets = combinations(i, length)
        for j in subsets:
            if(frozenset(j) not in prevFreqSet):
                temp_candidate_Set.remove(i)
                break
    return temp_candidate_Set

def above_min_sup(itemSet, data_list, min_sup, global_ItemSet_sup):
    freqItem_Set = set()
    local_ItemSet_Sup = defaultdict(int)

    for item in itemSet:
        for itemSet in data_list:
            if item.issubset(itemSet):
                global_ItemSet_sup[item] += 1
                local_ItemSet_Sup[item] += 1

    for item, supCount in local_ItemSet_Sup.items():
        support = float(supCount / len(data_list))
        if(support >= min_sup):
            freqItem_Set.add(item)

    return freqItem_Set