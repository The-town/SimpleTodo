# Simple Todo

[日本語のREADME](./doc/README-JA.md)

## Overview

**Simple Todo** is a to-do application using a text file.

![todo_public_ver_1](./doc_img/todo_public_ver_1.png)

## Usage

1. You register a folder that **Simple Todo** searches.
2. Put the string **[todo]** at the beginning of the file name in the folder.
3. If the file name contains the string **[todo]**, **Simple Todo** will display the 
   file in the list screen.
   If the file is a text file, it will be displayed on the detail screen.

_The string you use does not have to be **[todo]**._  
_You can specify any string in the configuration file._

## Features

### Use text files for data storage

The use of text files has improved data reusability and portability.
Even if you don't use **Simple Todo** anymore, todo will remain.

### Simple

Compare to other todo applications, **Simple Todo** is very simple. 

* Add todo
* Display todo list
* Display todo detail
* Coloring by important
* Sort by limit or important
* Filtering by folder

## How to Start

### Configuration

The Configuration file is **config.ini**.
The format is the following.

```ini
[Dir_names]
# name=path
# "name" is displayed in a select folder that right-clicks.
# example
# F:\Document\example
example=F:\Document\example

[File_names]
# String which this application searches for display files to list screen.
# Can use wildcard (*).

# example
# Head "todo"
todo=todo*

# python file
python=*.py

[Importance_color]
# "A" and "B", "C" express importance.
# A > B > C
# These strings contain a file name.
# [todo][A]example.txt
#
# "default" will use when not specified string.
#
# Color specifies string such as white or red, yellow or HEX.
default=white
A=red
B=#edea99
C=#37bc87

[Meta_data]
# Metadata index and key.
# [todo][A][#metadata1][#metadata2]example.txt
# You set metadata such as [#metadata].
# example: [#2020/09/01][#Add Function]example.txt -> limit:2020/09/01 category:Add Function
#          [#][#Add Function]example.txt -> category:Add Function
limit=limit
category=category

[Mail]
# メール関連の設定
imap_server=imap.example
user=hogehoge
password=password

[AddTodoFromMail]
# TODOファイルとして作成したい送信元メールアドレス
address=hogehoge@example
dir_path=F:\Document\todo\mail
```

**Note: when editing config.ini**

- You specify folder names to **Dir_names**.
- You specify file names to **File_names.**
- You can add **File_names** with the wild card "*".
- When multi names on File_names, will be a search for "OR".
- When specified **Importtance_color**, you add strings to the file name.
  - For Example, A=red file, names=[A]hogehoge.txt


### How to Run

> python display.py

## Document

[Simple Todo で実現したいこと](./doc/SimpleTodoで実現したいこと.md)

