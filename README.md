# SimpleTodo

## 概要

**SimpleTodo**とはテキストファイルを使用したTODO管理アプリケーションです。
やるべきことを忘れないようにでき、やりたいことを残せるようになります。



![todo_public_ver_1](./doc_img/todo_public_ver_1.jpg)



## 使い方

1. 普段使っているフォルダを**SimpleTodo**へ登録します。
2. フォルダの中にある、これから作業する予定のファイル名の先頭に**[todo]**という文字列を入れます。
3. **[todo]**という文字列がファイル名にある場合、**SimpleTODO**はそのファイルを一覧画面へ表示します。また、テキストファイルの場合はその内容を詳細画面へ表示します。



> 使用する文字列は[todo]出なくても構いません。任意の文字列を指定可能です。



## 特徴

### データの保管にテキストファイルを使用

テキストファイルを使用することでデータの再利用性・移行性を高めました。  
また、テキストファイルの操作は他のアプリケーションからも容易です。

TODOを記録したテキストファイルはこのアプリケーション以外からでも読み込めます。
このアプリケーションを使わなくなっても、あなたが行ってきたTODOは残るのです。

### 単純さ

他のTODOアプリケーションに比べて機能はずっと少ないです。  

* TODO追加
* TODOの一覧表示
* 重要度での色分け
* 期限・重要度での並び替え
* TODOの詳細確認


### 実装

Pythonのみで実装されています。  
GUI部分はTkinterを使用しています。



## 始め方



### 設定

設定ファイルは**config.ini**という名前のファイルで以下のフォーマットで記載します。

```ini
[Dir_names]
#プルダウンに表示される名前=TODOファイルを格納しているフォルダの絶対パス
#例
#F:\Document\800_IT自己学習\09_python\51_QiitaというフォルダにTODOファイルを格納する場合
qiita=F:\Document\800_IT自己学習\09_python\51_Qiita

[File_names]
#TODOリスト一覧に表示したいファイル名。ワイルドカード(*)を使用できます。
#例

#先頭にtodoという文字列があるファイル
todo=todo*

#拡張子がpyのファイル
python=*.py

[Importance_color]
#重要度を表すためにファイル名で使用する文字列と対応する色
#defaultは重要度の文字列が入っていないファイルに対して使用される色です。
#色はredやblueなどの文字列で指定します。
default=white
A=red
B=yellow
C=green

[Meta_data]
#メタデータとして使用するファイル内の文字列の位置とメタデータのキー名
#TODOファイルのファイル名のうち[#metadata]のように、[]で囲まれた#で始まる文字をメタデータとして認識します。
# example: [#2020/09/01][#機能追加]example.txtとすれば期限:2020/09/01 カテゴリ:機能追加となります。
#          [#][#機能追加]example.txtとすればカテゴリ:機能追加となります（#しかないため期限は無視される）。
1=期限
2=カテゴリ
```



**config.ini**を編集する際の注意点になります。

- **Dir_names**には複数のフォルダ名を記載できます。
- **File_names**には複数のファイル名を記載できます。
- ファイル名を記載する場合はワイルドカード（*）を使用できます。
- ファイル名を複数記載した場合は**or**の検索になります。
- **Importance_color**で指定した色にする場合は、ファイル名に**[文字列]**を加えます（例：**A=red**とした場合は、**[A]hogehoge**というファイル名にする）。

**※1  記載したフォルダ名配下に大量のフォルダ、ファイルがある場合、検索するのに時間がかかる場合があります。**
 **極端な話ですがフォルダ名にC:\と記載すると、TODOリストを表示するまでにかなりの時間を要します。**

**※2  TODOファイルの文字コードはUTF-8にしてください。詳細画面が表示されません。**



### 実行方法

> python display.py

