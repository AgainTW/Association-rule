import associate_rule
import fptree
import csv

def fit():
    d2C_data_name_path = "inputs/ibm-2021.txt"
    temp1, temp2, support, confidence, lift = fptree.fit(d2C_data_name=d2C_data_name_path, d2C_save_name='data/0_d2C_save.csv', first_scan_name='data/1_first_scan.csv', limit=2, limit_cut_name='data/2_limit_cut.csv', sort_name='data/3_sort.csv', new_data_name='data/4_new_data.csv')
#    print(len(support),len(confidence),len(lift))

    with open("data/temp1.csv", 'w', newline='') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        # 寫入列資料
        for i in temp1:
            writer.writerow([i])

    with open("data/temp2.csv", 'w', newline='') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        # 寫入列資料
        for i in temp2:
            writer.writerow([i])

    with open("data/support.csv", 'w', newline='') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        # 寫入列資料
        for i in support:
            writer.writerow([i])

    with open("data/confidence.csv", 'w', newline='') as csvfile2:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile2)
        # 寫入列資料
        for i in confidence:
            writer.writerow([i])

    with open("data/lift.csv", 'w', newline='') as csvfile3:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile3)
        # 寫入列資料
        for i in lift: 
            writer.writerow([i])
