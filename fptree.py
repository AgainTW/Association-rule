import associate_rule
import np

# 把所有東西整理在一起
def fit(d2C_data_name=None, d2C_save_name=None, first_scan_name=None, limit=None, limit_cut_name=None, sort_name=None, new_data_name=None):
	# .data檔處理成.csv
	associate_rule.data2csv(d2C_data_name, d2C_save_name)

	# 1.對data做first_scan並儲存
	test_data = associate_rule.csv2list(d2C_save_name)
	test_data = np.array(test_data)
	test_data = test_data[1:,:]
	data_1 = associate_rule.first_scan(test_data)
	data_label = ['Item ID', 'times']
	associate_rule.list2csv(first_scan_name, data_1, data_label)

	# 2.將first_scan中次數太低的刪除
	data_2 = associate_rule.csv2list(first_scan_name)
	data_2 = np.array(data_2)
	data_2 = data_2[1:,:]
	data_2 = associate_rule.limit_cut(data_2, limit)
	associate_rule.list2csv(limit_cut_name, data_2, data_label)

	# 3.對limit_cut後的資料做排序
	data_3 = associate_rule.csv2list(limit_cut_name)
	data_3 = associate_rule.mergeSort(data_3[1:])
	associate_rule.list2csv(sort_name, data_3, data_label)

	# 4.將data整理成可以餵進去fp_tree的形式
	data_4 = associate_rule.csv2list(sort_name)
	data_4 = np.array(data_4)
	data_4 = data_4[1:,:]
	data_4 = associate_rule.tidy_data(test_data, data_4)
	associate_rule.list2csv(new_data_name, data_4)
	
	# 建立 fp tree 和 frequency table
	data_5 = associate_rule.csv2list(sort_name)
	data_5 = data_5[1:][:]
	data_6 = associate_rule.csv2list(new_data_name)
	tree_head = associate_rule.fp_tree(data_6)
	head_table_dummy = associate_rule.Header_Table(tree_head, data_5)
#	print("完成0")


	# 計算出各項數值
	frequent_patterns = []
	frequent_patterns_count = []

	frequent_patterns, frequent_patterns_count = associate_rule.find_path(tree_head, head_table_dummy)
#	print("完成1")
	divid_list = associate_rule.divid_path(frequent_patterns, frequent_patterns_count)
#	print("完成2")
	fp = associate_rule.tidy_path(divid_list, limit)
	associate_rule.list2csv("data/fp.csv", fp)
#	print("完成3")

	# 將只有單筆的資料加入
	for i in data_3:
		fp.append([int(i[1]),i[0]])

	temp1 = []
	temp2 = []
	temp3 = []
	support = associate_rule.support(fp, test_data[-1][0] )
#	print("完成4")
	
	temp1, temp2, support_2, confidence = associate_rule.confidence(fp, support)
#	print("完成5")

	lift = associate_rule.lift(fp, temp1, temp2, support, confidence)
#	print("完成6")
	
	return temp1, temp2, support_2, confidence, lift
