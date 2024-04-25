# kraken2composition

kraken2形式のテーブルを系統組成のrank,taxonomyの階層のjsonに変換します



## input形式

以下のようなヘッダを持ったkraken2の出力形式を持ったcsvファイルを入力として想定しています。

```
count,superkingdom,phylum,class,order,family,genus,species,strain,filename,sig_name,sig_md5,total_counts
```

### 出力

対象となるディレクトリからファイル名を収集しRUN IDに変換したうえで
RUNに紐づく組成データをBioProjectにネストしたデータ構造として出力します。


```
{
"bioproject": "PRJDB0000",
"compositions":
    [
        {
            "run":"DRR0000",
            "ranks":{
                phylum: {
                    "composition":{
                        "taxonomy 1": num,
                        "taxonomy 2": num,
                    }
                },
                class: {
                    "composition":{
                        "taxonomy 1": num,
                        "taxonomy 2": num,
                    }
                },,
            }
            
        },
    ]
} 
```


## 環境


## 利用方法

- ファイルを指定して変換


- ディレクトリを指定して変換



