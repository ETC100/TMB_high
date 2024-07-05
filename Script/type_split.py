import sys
import re
import argparse
import pandas as pd


def read_file(file_path):
    df = pd.read_csv(file_path, sep='\t')
    return df

def merge_file(df1, df2):
    data = df1
    data['sample_id'] = data['Link'].apply(extract_sample_id)
    data["sample_name"] = data['sample_id'].str.split('_').str[1]
    info = df2
    merged_df = pd.merge(df1, df2, on="sample_name")
    return merged_df

def split_store(merged_file, store_path):
    df = merged_file
    # 根据类型列将数据分割成不同的子数据框
    dfs = {}
    for type_val, group in df.groupby('cancer_type'):
        dfs[type_val] = group

    # 将每个子数据框存储为单独的文件
    for type_val, sub_df in dfs.items():
        file_name = f"{type_val}_data.tsv"
        output_path = store_path + '/' + file_name
        sub_df.to_csv(output_path, index=False, sep='\t', encoding='utf')
        print(f"保存 {type_val} 类型数据到 {file_name}")

def extract_sample_id(link):
    match = re.search(r'b=([^&]+)', link)
    if match:
        return match.group(1)
    return None

def main():
    data = read_file(r'D:\cancer_type\total_autofilter.csv')
    info = read_file(r'D:\cancer_type\number_type.list')
    merged_file = merge_file(data, info)
    split_store(merged_file, r'D:\cancer_type')

if __name__ == '__main__':
    main()
