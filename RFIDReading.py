import csv
import os


input_file = r'C:\Users\mugia\OneDrive\デスクトップ\Work\Study\PreInput.csv'
output_file = r'C:\Users\mugia\OneDrive\デスクトップ\Work\Study\PreOutput.csv'

#すでにラベル付けされているデータを読み込む
labeled_data = {}
if os.path.isfile(output_file):
    with open(output_file, 'r', encoding = 'utf-8') as outfile:
        reader = csv.reader(outfile)
        next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            rfid_id, label = row[0], row[1]
            labeled_data[rfid_id] = label

#24文字ごとにデータを分割する関数
def split_data(data_string):
    return [data_string[i:i+24] for i in range(0, len(data_string), 24)]

#新しいデータにラベル付け
with open(input_file, 'r', encoding = 'utf-8') as infile, open(output_file, 'a', newline = '', encoding= 'utf-8') as outfile:
    #CSVリーダーとライターを作成
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    #初回実行時にヘッダーを出力
    if os.stat(output_file).st_size == 0:
        header = next(reader)
        writer.writerow(header + ['ラベル'])
    else:
        next(reader)

    #各行を24文字ごとに分割し、各IDにラベル付け
    for row in reader:
        if len(row) == 0:
            continue
        data_string = row[0]

        #24文字ごとに分割
        rfid_ids = split_data(data_string)
        
        for rfid_id in rfid_ids:
            if rfid_id in labeled_data:
                continue
            print(f"データ：{rfid_id}")
            label = input("このデータに対するラベルを入力してください")    
            writer.writerow([rfid_id, label])


