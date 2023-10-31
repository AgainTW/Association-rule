import csv
import np

# linked-list
#done# 定義linked-list
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.nextitr = []						#可指向多個下一個位置
        self.father = None						#指向父節點
        self.count = 1
    def itr_save(self,next):
    	self.nextitr.append(next)
    	next.father = self

# 資料前處理
#done# 將.data轉.csv
def data2csv(data_name, save_name):
	data_file = open(data_name,'r')

	temp = []
	for i in data_file:
		temp.append(str(i).split())

	with open(save_name, 'w', newline='') as csvfile:
		# 建立 CSV 檔寫入器
		writer = csv.writer(csvfile)
		writer.writerow(["Customer ID", "Transaction ID", "Item ID"])
		# 寫入列資料
		for i in range( len(temp) ):
			writer.writerow( [temp[i][0], temp[i][1], temp[i][2]] )

#done# 將.csv轉list
def csv2list(data_name):
	with open(data_name, newline='') as csvfile:
		rows = csv.reader(csvfile)
		temp = []

		for row in rows:
			temp.append(row)
		return temp

#done# 將list轉.csv 避免測試時一直重複計算
def list2csv(data_name, data, data_label=None):
	with open(data_name, 'w', newline='') as csvfile:
		# 建立 CSV 檔寫入器
		writer = csv.writer(csvfile)

		if(data_label!=None):	writer.writerow(data_label)
		# 寫入列資料
		for i in range( len(data) ):
			writer.writerow(data[i][:])



# FP-tree
#done#	第一次掃描，建立ID和出現次數list
def first_scan(data):
	temp_name = []
	temp_count = []
	data2 = []
	temp_count2 = 0
	search_falg = 1

	data2.append([data[0][0], data[0][1]])
	temp_name.append(data[0][2])
	temp_count.append(1)	

	for i in range( len(data) ):
		search_falg = 1		
		for j in range( len(temp_name) ):
			if( search_falg==1 ):			
				if( data[i][2] != temp_name[j] ):	temp_count2 += 1
				elif( data[i][2] == temp_name[j] ):	
					temp_count[j] = temp_count[j] + 1
					temp_count2 = 0
					search_falg = 0
		if( temp_count2 == len(temp_name) ):
			temp_name.append(data[i][2])
			temp_count.append(1)
			search_falg = 0
			temp_count2 = 0	

	data2 = np.stack((temp_name, temp_count), axis=1 )
	return data2

#done# 刪除不達下限的資料
def limit_cut(data, limit):
	temp = []
	for i in range(1,len(data)):
		if( int(data[i][1]) > limit ):	temp.append([data[i][0], data[i][1]])
	return temp

#done# mergesort
def mergeSort(arr):
	if len(arr) <= 1:		return arr	

	# Finding the mid of the array
	mid = len(arr)//2

	# Dividing the array elements into 2 halves
	L = arr[:mid][:]
	R = arr[mid:][:]
 
	# Sorting the first half and second half
	L = mergeSort(L)
	R = mergeSort(R)

	return merge(L,R)

def merge(L,R):
	L_index,R_index = 0,0
	merge_list = []

	# 判斷列表裡面是否還有元素可以用
	while L_index < len(L) and R_index < len(R):
	# 哪邊的元素小於另外一邊的的元素就把哪邊的元素加入進去，對應的索引加一
		if( int(L[L_index][1])>int(R[R_index][1]) ):
			merge_list.append([L[L_index][0],L[L_index][1]])
			L_index += 1
		else:
			merge_list.append([R[R_index][0],R[R_index][1]])
			R_index += 1
	# 下面的這兩個就是，如果有一個列表全部添加了，另外一個列表直接新增到merge_list裡面了
	merge_list += L[L_index:]
	merge_list += R[R_index:]
	
	return merge_list

#done# 將資料整理成對應格式
def tidy_data(data, goal):
	temp_1 = []
	temp_2 = []
	customer_flag = 0

	for i in data:
		if( customer_flag==0 ):	customer_flag = i[0]
		elif( customer_flag!=i[0] ):
			if( len(temp_1)>1 ):	temp_2.append(temp_1)
			temp_1 = []
			customer_flag = i[0]

		for j in goal:
			if( i[2]==j[0] ):	temp_1.append(i[2])
	return temp_2

#done# 搜尋所有子節點
def search_kid(dummyHead, data):					#將兒子遍歷
	flag = 0
	for i in dummyHead.nextitr:							#找兒子
		if( i.val == data ):							#有找到
			flag = 1
			return flag,i
	return flag,dummyHead								#沒找到

#done# 將樹全部印出
def print_all(root, val_flag=1, nextitr_flag=None, father_flag=None, count_flag=None):
	# 計算root的BFS路徑
	curr = root
	stack = []
	save_all = []
	if( len(curr.nextitr)!=0 ):	stack.append(curr)
	while( len(stack)>0 ):
		curr = stack.pop(0) 
		save_all.append(curr)		#將路徑儲存
		for i in curr.nextitr:
			stack.append(i)

	# 根據save_all遍歷
	for i in save_all:
		if(val_flag): print(i.val, end=" ")
		if(nextitr_flag):	print(i.nextitr, end=" ")
		if(father_flag):	print(i.father, end=" ")
		if(count_flag):	print(i.count, end=" ")
		print("\n")

#done# 建fp tree
def fp_tree(data):
	# 指標建立
	dummyHead = ListNode(0)
	curr = dummyHead

	for i in data:
		curr = dummyHead									#將curr指回樹根
		for j in i:
			flag,curr = search_kid(curr, j)

			if( flag == 1 ):
				curr.count += 1
			elif( flag == 0 ):
				newNode = ListNode(j)      					#生成新的linked list資料
				curr.itr_save(newNode)                      #curr指到新的linked list位置
				curr = newNode
	return dummyHead

#done# 建關聯表
def Header_Table(fpHead, goal):
	# 生成初始Header Table
	Header_Table_dummyHead = ListNode(0)
	curr = Header_Table_dummyHead
	for i in goal:
		newNode = ListNode(i[0])
		curr.itr_save(newNode)	

	# 計算fpHead的BFS路徑
	curr = fpHead
	stack = []
	save_all = []
	if( len(curr.nextitr)!=0 ):	stack.append(curr)
	while( len(stack)>0 ):
		curr = stack.pop(0) 
		save_all.append(curr)		#將路徑儲存
		for i in curr.nextitr:
			stack.append(i)

	# 根據Header_Table找路徑
	for i in Header_Table_dummyHead.nextitr:
		for j in save_all:
			if( i.val==j.val ):	i.nextitr.append(j)

	return Header_Table_dummyHead



# Frequent Patterns
### 根據 frequent table 從 fp tree 中出所有路徑(包含次數)
def find_path(fpHead, goal):
	# 變數設定
	frequent_patterns = []
	frequent_patterns_count = []
	temp = []
	temp_2 = []
	count = 0

	# 根據 father 一路 trace 回 fpHead 的 dummy head
	for i in range(len(goal.nextitr)):
		count = 0
		curr_1 = goal.nextitr[ len(goal.nextitr)-i-1 ]
		for j in curr_1.nextitr:
			curr_2 = j
			while( curr_2!=fpHead ):
				temp.append(curr_2.val)
				temp_2.append(j.count)
				curr_2 = curr_2.father
			frequent_patterns.append(temp)
			frequent_patterns_count.append(temp_2)
			temp = []
			temp_2 = []
	return frequent_patterns, frequent_patterns_count

### 產生能分解path的參照數列(有一個固定)
def gen_seq(d_len):
    temp = 0
    temp_1 = []
    temp_2 = []
    if(d_len==0):   temp_2.append([1])
    else:
        for i in range(1,2**d_len):
            temp_1 = []
            temp = i
            while(temp != 0):
                temp_1.append( temp%2 )
                temp = temp//2   
            while( len(temp_1)<d_len ):
                temp_1.append(0)
            temp_1.append(1)
            temp_1.reverse()
            temp_2.append(temp_1)
    return temp_2

### 第二種能產生分解path的參照數列(沒有固定)
def gen_seq2(d_len):
    temp = 0
    temp_1 = []
    temp_2 = []
    if(d_len==1):   temp_2.append([1])
    else:
        for i in range(1,2**d_len-1):
            temp_1 = []
            temp = i
            while(temp != 0):
                temp_1.append( temp%2 )
                temp = temp//2   
            while( len(temp_1)<d_len ):
                temp_1.append(0)
            temp_1.reverse()
            temp_2.append(temp_1)
    return temp_2

### 分解 find_path 找到的資料
def divid_path(freq_pat, freq_pat_count):
	temp = []  							# 儲存分解的資料
	temp_sub = []						# temp 的預儲存
	temp_2 = []
	temp_3 = 0
	for i in range(len(freq_pat)):
		seq = gen_seq(len(freq_pat[i])-1)
		temp_2 = freq_pat[i]
		for j in seq:
			temp_sub.append(freq_pat_count[i][0])
			for k in range(len(j)):
				if(j[k]==1):    temp_sub.append(temp_2[k])
			temp.append(temp_sub)
			temp_sub = []
		temp_3 = temp_3 + len(seq)
	return temp

### 將 divid_path 
def tidy_path(divid_list, limit):
	temp_1 = []
	temp_2 = []
	temp_3 = []
	flag = -1

	for i in range(len(divid_list)):
		if( flag==-1 ):	
			flag = divid_list[i][1]
			temp_1.append(divid_list[i])
		elif( divid_list[i][1]==flag ):	
			temp_1.append(divid_list[i])
		else:
			flag = divid_list[i][1]
			temp_2 = section_tidy_path(temp_1)
			for j in temp_2:
				temp_3.append(j)
			temp_2 = []
			temp_1 = []
			temp_1.append(divid_list[i])

	temp_4 = []
	for i in temp_3:
		if( i[0]>limit ):	temp_4.append(i)
	temp_5 = []
	for i in temp_4:
		if( len(i)>2 ):	temp_5.append(i)
	
	return temp_5

def section_tidy_path(divid_list):
	temp = []
	flag = 0
	for i in divid_list:
		flag = 0
		for j in temp:
			if( len(i[1:])==len(j[1:]) and i[1:]==j[1:] ):	
				j[0] = j[0]+i[0]
				flag = 1
		if( flag!=1 ):
			flag = 0
			temp.append(i)
	return temp



# 數值計算
### support，其中trans_num為總交易數
def support(fp, trans_num):
	support = []
	for i in fp:
		support.append( i[0]/int(trans_num) )
	return support

### confidence
def confidence(fp, support):
	confidence = []
	temp1 = []
	temp2 = []
	support_2 = []
	temp_sub1 = []
	temp_sub2 = []
	temp_2 = []

	# 將fp分割
	for i in range(len(fp)):
#		if( i%(len(fp)//10)==0 ):	print(i/len(fp))			# 判斷程式進度用
		seq = gen_seq2(len(fp[i])-1)
		temp_2 = fp[i]
		for j in seq:
			for k in range(len(j)):
				if(j[k]==1):	temp_sub1.append(temp_2[k+1])
				else :	temp_sub2.append(temp_2[k+1])
			temp1.append(temp_sub1)
			temp2.append(temp_sub2)
#			print(j,"  ",temp_sub1,"  ",temp_sub2)				# 測試用
			support_2.append(support[i])
			temp_sub1 = []
			temp_sub2 = []

	# 根據分割計算confidence
	temp3 = 0
	count = 0
	for i in range(len(temp1)):
#		if( i%(len(temp1)//10)==0 ):	print(i/len(temp1))		# 判斷程式進度用
		for j in fp:
			if( j[1:]==temp1[i] ):  temp3 = support[count]
			count = count + 1
		if( temp3==0 ):	confidence.append(0)
		else:	confidence.append(support_2[i]/temp3)
		count = 0
		temp3 = 0

	return temp1, temp2, support_2, confidence

### lift
def lift(fp, temp1, temp2, support, confidence):
	lift = []
	temp = 0
	count = 0
	for i in range(len(temp1)):
#		if( i%(len(temp1)//10)==0 ):	print(i/len(temp1))		# 判斷程式進度用
		for j in fp:
			if( j[1:]==temp2[i] ):	temp = support[count]
			count = count + 1
		if( temp!=0 ): 		lift.append(confidence[i]/temp)
		count = 0
		temp = 0
	return lift