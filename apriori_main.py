import apriori
import associate_rule
import np
import csv
import np

def fp_divid(fp, support):
    temp1 = []
    temp2 = []
    support_2 = []
    temp_sub1 = []
    temp_sub2 = []
    temp_2 = []
    for i in range(len(fp)):
        seq = associate_rule.gen_seq2(len(fp[i])-1)
        temp_2 = fp[i]
        for j in seq:
            for k in range(len(j)):
                if(j[k]==1):    temp_sub1.append(temp_2[k+1])
                else :  temp_sub2.append(temp_2[k+1])
            temp1.append(temp_sub1)
            temp2.append(temp_sub2)
            support_2.append(support[i])
            temp_sub1 = []
            temp_sub2 = []
    return temp1, temp2, support_2

def fit():
    # 讀資料
    data_1 = associate_rule.csv2list("data/4_new_data.csv")
    data_2 = associate_rule.csv2list("data/3_sort.csv")
    data_3 = associate_rule.csv2list("data/2_limit_cut.csv")
    data_4 = associate_rule.csv2list("data/1_first_scan.csv")
    data_4 = np.array(data_4)
    data_4 = data_4[1:,:]
    fp = associate_rule.csv2list("data/fp.csv")
    support_data = associate_rule.csv2list("data/support.csv")

    # 計算confidence
    global_FreqItem_Set, rules = apriori.apriori(data_1, 0.0055, 0)
    confidence = []
    for i in rules:
        confidence.append(i[2])

    # 計support
    ### temp1 & temp2 整成 set
    temp1, temp2, temp_support = fp_divid(fp, support_data)
    col_1 = []
    set_temp1 = []
    set_temp2 = []
    order = []
    for i in range(len(temp1)):
        set_temp1 = set([j for j in temp1[i]])
        set_temp2 = set([j for j in temp2[i]])
        col_1.append([set_temp1,set_temp2])
    for i in rules:
        count = 0
        for j in col_1:
            if( j[0]==i[0] and j[1]==i[1] ):    order.append(count)
            count += 1
    support = []
    for i in order:
        support.append(temp_support[i])

    # 計算lift
    lift = []
    support_count = []
    flag = 0
    for i in data_3:
        if(flag):   fp.append([int(i[1]),i[0]])
        flag += 1
    for i in fp:
        support_count.append( int(i[0])/int(data_4[-1][0]) )
    for i in range(len(confidence)):
        count = 0
        for j in fp:
            set_temp3 = set([k for k in j[1:]])
            if(rules[i][1]==set_temp3):
                lift.append(confidence[i]/support_count[count])
            count += 1

    # 輸出整理
    col = []
    for i in rules:
        col.append(str(i[0])+' -> '+str(i[1]))
    final = []
#    final.append(["relationship", "support", "confidence", "lift"])
    for i in range(62):
        final.append([col[i], support[i][0], confidence[i], lift[i]])
    return final
#    associate_rule.list2csv("ibm-2021-appriori.csv",final)