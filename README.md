# Simple Todo

[���{���README](./doc/README-JA.md)

## Overview

**Simple Todo** is todo application using text file.

![todo_public_ver_1](./doc_img/todo_public_ver_1.png)

## Usage

1. You register folder which **Simple Todo** search.
2. Put the string **[todo]** at the beginning of the file name in the folder.
3. If the file name contains the string **[todo]**, **Simple Todo** will display the 
file in the list screen.
   If the file is a text file, it will be displayed in the detail screen.
   
_The string you use does not have to be **[todo]**._  
_You can specify any string in the configuration file._

## Features

### Use text files for data storage

The use of text files has improved data reusability and portability.
Even if you don't use **Simple Todo** anymore, todo will remain.

### Simple

Compare other todo application, **Simple Todo** is very simple. 

* Add todo
* Display todo list
* Display todo detail
* Coloring by important
* Sort by limit or important
* Filtering by folder

## How to Start

### Configuration

Configuration file is **config.ini**.
Format is following.

TODO Japanese to English

```ini
[Dir_names]
# name=path
# "name" is displayed name in select folder which right click.
# example
# F:\Document\example
example=F:\Document\example

[File_names]
# String which this application search for display file to list screen.
# Can use wildcard (*).

# example
# Head "todo"
todo=todo*

# python file
python=*.py

[Importance_color]
# "A" adn "B", "C" express importance.
# A > B > C
# These string contain file name.
# [todo][A]example.txt
#
# "default" will use when not specified string.
#
# Color specify string such as white or red, yellow or HEX.
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
```

**config.ini**��ҏW����ۂ̒��ӓ_�ɂȂ�܂��B

- **Dir_names**�ɂ͕����̃t�H���_�����L�ڂł��܂��B
- **File_names**�ɂ͕����̃t�@�C�������L�ڂł��܂��B
- �t�@�C�������L�ڂ���ꍇ�̓��C���h�J�[�h�i*�j���g�p�ł��܂��B
- �t�@�C�����𕡐��L�ڂ����ꍇ��**or**�̌����ɂȂ�܂��B
- **Importance_color**�Ŏw�肵���F�ɂ���ꍇ�́A�t�@�C������ **[������]** �������܂��i��F **A=red** �Ƃ����ꍇ�́A **[A]hogehoge** �Ƃ����t�@�C�����ɂ���j�B

**��1  �L�ڂ����t�H���_���z���ɑ�ʂ̃t�H���_�A�t�@�C��������ꍇ�A��������̂Ɏ��Ԃ�������ꍇ������܂��B**
 **�ɒ[�Șb�ł����t�H���_����C:\�ƋL�ڂ���ƁATODO���X�g��\������܂łɂ��Ȃ�̎��Ԃ�v���܂��B**

**��2  TODO�t�@�C���̕����R�[�h��UTF-8�ɂ��Ă��������B�ڍ׉�ʂ��\������܂���B**

### How to Run

> python display.py

## Document

[Simple Todo �Ŏ�������������](./doc/SimpleTodo�Ŏ�������������.md)

