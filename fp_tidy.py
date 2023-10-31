import associate_rule

def fit():
	temp1 = associate_rule.csv2list("data/temp1.csv")
	temp2 = associate_rule.csv2list("data/temp2.csv")
	support_temp = associate_rule.csv2list("data/support.csv")
	confidence_temp = associate_rule.csv2list("data/confidence.csv")
	lift_temp = associate_rule.csv2list("data/lift.csv")

	# 第一行處理
	col_1_temp1 = []
	col_1_temp2 = []
	col_1 = []
	### 處理左側
	for i in temp1:
		for j in i:
			col_1_temp1.append('{'+j[1:-1]+'}'+' -> ')
	### 處理右側
	for i in temp2:
		for j in i:
			col_1_temp2.append('{'+j[1:-1]+'}')
	### 合併左右側
	for i in range(len(col_1_temp1)):		
		col_1_temp1[i] = col_1_temp1[i] + col_1_temp2[i]
	### 去掉左側沒值的
	for i in col_1_temp1:
		if( i[-2:]!="{}" ):		col_1.append(i)


	# 第二行處理
	count = 0
	support = []
	for i in support_temp:
		if( count<62 ):		support.append(i[0])
		count = count + 1


	# 第三行處理
	count = 0
	confidence = []
	for i in confidence_temp:
		if( count<62 ):		confidence.append(i[0])
		count = count + 1


	# 第三行處理
	count = 0
	lift = []
	for i in lift_temp:
		lift.append(i[0])


	final = []
#	final.append(["relationship", "support", "confidence", "lift"])
	for i in range(62):
		final.append([col_1[i], support[i], confidence[i], lift[i]])
		
	return final
#	associate_rule.list2csv("ibm-2021-fp_growth.csv",final)


