import csv
import os

# ファイルパス設定
INPUT_FILE = r'C:\Users\mugia\OneDrive\デスクトップ\Work\Study\PreInput.csv'
OUTPUT_FILE = r'C:\Users\mugia\OneDrive\デスクトップ\Work\Study\PreOutput.csv'
PROCESSED_FILE = r'C:\Users\mugia\OneDrive\デスクトップ\Work\Study\input_noduplication_file.csv'

# ラベル付け済みデータを読み込む
def load_labeled_data(output_file):
    labeled_data = {}
    if os.path.isfile(output_file):
        with open(output_file, 'r', encoding='utf-8') as outfile:
            reader = csv.reader(outfile)
            next(reader, None)  # ヘッダーをスキップ
            for row in reader:
                if len(row) >= 2:
                    rfid_id, label = row[0], row[1]
                    labeled_data[rfid_id] = label
    return labeled_data

# 24文字ごとにデータを分割する
def split_data(data_string):
    return [data_string[i:i+24] for i in range(0, len(data_string), 24)]

# 重複を削除する
def remove_duplicates(data_list):
    return sorted(set(data_list))  # 重複削除後ソート

# 全角を半角に変換する
def convert_to_half_word(text):
    return unicodedate.normalize('NFKC', text)

# 入力データを処理し、分割＆重複削除結果を保存
def preprocess_input(input_file, processed_file):
    unique_ids = set()
    if os.path.isfile(input_file):
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            next(reader, None)  # ヘッダーをスキップ
            for row in reader:
                if row:
                    split_ids = split_data(row[0])  # 24文字ごとに分割
                    unique_ids.update(split_ids)  # 集合に追加

    # ファイルに保存
    with open(processed_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["RFID_ID"])  # ヘッダー
        for unique_id in remove_duplicates(list(unique_ids)):
            writer.writerow([unique_id])

# ラベル付けを行う
def label_data(processed_file, output_file, labeled_data):
    with open(processed_file, 'r', encoding='utf-8') as infile, open(output_file, 'a', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 初回実行時にヘッダーを出力
        if os.stat(output_file).st_size == 0:
            writer.writerow(["RFID_ID", "ラベル"])

        # ラベル付け処理
        next(reader, None)  # ヘッダーをスキップ
        for row in reader:
            if len(row) == 0:
                continue
            rfid_id = row[0]

            # ラベル付け済みの場合はスキップ
            if rfid_id in labeled_data:
                continue

            # ラベル付け
            print(f"データ：{rfid_id}")
            label = input("このデータに対するラベルを入力してください：")
            writer.writerow([rfid_id, label])

# メイン処理
def main():
    # ラベル済みデータをロード
    labeled_data = load_labeled_data(OUTPUT_FILE)

    # 入力データを処理して保存
    preprocess_input(INPUT_FILE, PROCESSED_FILE)

    # ラベル付けを実施
    label_data(PROCESSED_FILE, OUTPUT_FILE, labeled_data)

if __name__ == "__main__":
    main()
