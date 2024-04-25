import csv
import os
import glob
from typing import List, NewType
import argparse
import re

Filepath = NewType("Filepath", str)

# kraken2 reportのヘッダ
headers = ["count", "superkingdom", "phylum", "class", "order", "family", "genus", "species", "strain"
           "filename", "sig_name", "sig_md5", "total_counts"]
# 出力する階級をリストで指定
ranks = ["phylum", "class", "order", "family", "genus", "species"]

def get_args():
    parser = argparse.ArgumentParser(description="This script takes in a directory of kraken2 output files and creates a composition file for each sample")
    parser.add_argument("-i", "--input", help="Path to input directory of kraken2 output files")
    parser.add_argument("-o", "--output", help="Path to output directory of composition files")
    return parser.parse_args()


def read_kraken2report(file_path: str) -> List[list]:
    """
    kraken2 reportファイル」を読みこんでlistを返す
    :return:
    """
    with open(file_path, "r") as f:
        d = csv.reader(f, delimiter=",")
        # 先頭行はヘッダ行
        rows = [row for row in d]
        return rows


def select_by_rank(rows: list, rank: str) -> List[list]:
    """
    rowsからその行の分類rankが引数で指定した値の行（count, taxonomy）だけを抽出して返す。
    rankの一致の判定は最も細分化されたrankが指定したrankかどうかを判定する。
    taxonomy nameはreportで付加されたprefixを除去して返す。
    :param rows:
    :param rank:
    :return:
    """
    # 引数で指定したrankのカラムの序数を取得する
    i = headers.index(rank)
    if i == -1:
        raise ValueError("rank is not found in headers")
    elif rank == "strain":
        # rank == "strain"のケースのみstrainのカラムに値がある行を返す. strainとspeciesのカラムの序数をハードコードしている
        selected_rows = [row for row in rows if row[7] != "" and row[8] != ""]
    else:
        # 指定したrankのカラムに値があり、rankの次のカラムに値がない行 = 指定したrankの値が含まれる行を抽出する
        # csvに空行が含まれるケースも想定されるため
        selected_rows = [row for row in rows if len(row) > 0 and row[i] != "" and row[i+1] == ""]

    # taxonomy nameのprefixを除去、countとtaxonomy nameのみのリストを返す
    selected_rows = [[row[i].split("__")[1], int(row[0])] for row in selected_rows]
    composition = {x[0]:x[1] for x in selected_rows if x[1] != ""}
    return {rank: composition}


def get_run_id(input_path: Filepath) -> str:
    """_summary_
    ファイル名からrun_idを取得する。
    想定するファイル名はrun id + _n.fastq.sam.mapped.bam...txtのような文字列なので
    ファイル名先頭のアルファベット＋数字分部分を利用する。
        file_name (_type_): _description_
    Returns: RUN ID
    """
    file_name = file_name.split("/")[-1]
    # 三頭のアルファベット＋数字分部分を取得
    run_id = re.findall(r'^[a-zA-Z0-9]+', file_name)
    return run_id[0]


def main():
    """
    kraken2形式のreportファイルを読みこみ、プロジェクト、分類階級、taxonomy、サンプルでまとめた組成データをJSON形式で出力する。
    """
    args = get_args()
    input_path = args.input
    output_path = args.output
    run = ""

    # 1. read kraken2 report and return as list of list
    rows = read_kraken2report(input_path)
    # 2. select by rank
    composition = {}
    for rank in ranks:
        composition.update(select_by_rank(rows, rank))
    return composition
    

if __name__ == "__main__":
    """_summary_
    サンプル（run）ごとの系統組成データを取得しdict形式に変換する
    """
    composition = main()
    print(composition)
