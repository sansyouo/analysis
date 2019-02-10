import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.constants as sc
import sys

f = open(sys.argv[1])
data_list = f.readlines() #ファイルを開いて一行ずつ読み込み
f.close()

f = open (sys.argv[2])
dark_list = f.readlines()
f.close()

data_list = [data_list.strip() for data_list in data_list] #改行記号の除去,dataファイルの絶対パス群
dark_list = [dark_list.strip() for dark_list in dark_list] #darkファイルの絶対パス群
dark_list_df = pd.DataFrame(dark_list, columns = ["col1"]) #darkファイルの絶対パス群DF
for n,file_name in enumerate(data_list): #enumerateで配列のインデックスと要素を取得
    file = pd.read_csv(data_list[n], header = None, sep = " ", names=("shift","Inte")) #ファイル開いたり
    #file_path = list[n][:38] + "darked/" + list[n][42:-4] + "-d.txt" #リネームしたり
    #search_str = list[n][29:37]
    file_path = data_list[n][:40] + "darked/" + data_list[n][44:-4] + "-d.txt" #リネームしたり
    search_str = data_list[n][65:70]
    print(dark_list_df)
    print(search_str)
    dark_files = dark_list_df[dark_list_df["col1"].str.contains(search_str)] #対象のファイルと同じ日付Dirのdarkデータの絶対パス群
    if "2000" in file_name:
        print(dark_files)
        same_count_file = dark_files[dark_files["col1"].str.contains("2000")] #darkデータで同じカウントのファイル見つけて
        print(same_count_file)
        same_count_file = same_count_file.col1.values[0] #そのファイルの絶対パスだけ取り出す
        dark_file = pd.read_csv(same_count_file, header = None, sep = " ", names = ("shift", "Inte"))
        darked_file = file["Inte"] - dark_file["Inte"]
    elif "4000" in file_name:
        same_count_file = dark_files[dark_files["col1"].str.contains("4000")] #darkデータで同じカウントのファイル見つけて
        same_count_file = same_count_file.col1.values[0] #そのファイルの絶対パスだけ取り出す
        dark_file = pd.read_csv(same_count_file, header = None, sep = " ", names = ("shift", "Inte"))
        darked_file = file["Inte"] - dark_file["Inte"]
    elif "6000" in file_name:
        print(dark_files)
        same_count_file = dark_files[dark_files["col1"].str.contains("6000")] #darkデータで同じカウントのファイル見つけて
        print(same_count_file)
        same_count_file = same_count_file.col1.values[0] #そのファイルの絶対パスだけ取り出す
        dark_file = pd.read_csv(same_count_file, header = None, sep = " ", names = ("shift", "Inte"))
        darked_file = file["Inte"] - dark_file["Inte"]
    else:
        print("うんこ")
    darked_file = pd.DataFrame(darked_file, columns = ["Inte"])
    darked_file = pd.concat([file["shift"], darked_file["Inte"]], axis = 1)
    darked_file.to_csv(file_path, header = None, index = None, sep = " ")
