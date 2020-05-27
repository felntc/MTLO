# インストール方法

## windowsの場合はexeファイルを利用できます
releasesからダウンロード

## python環境

### anaconda 仮想環境を利用する(推奨)  
1. 仮想環境を構築
```terminal
$ conda env create -n 新たな環境名 -f iromonea.yml
```
2. 切り替え
```terminal
$ conda activate [name]
```
3. 抜ける  
```terminal
$ conda deactivate
```

### pipで構築
***環境破壊の恐れがあるので注意してください***
- pip install opencv-python
- pip install keras
- pip install tensorflow
- pip install matplotlib
- pip install pandas
- pip install pysimplegui
- pip install websocket-client
- pip install pygame
