# Simple Todo

[���{���README](./doc/README-JA.md)

## Overview

**Simple Todo** is todo application using text file.

![todo_public_ver_1](./doc_img/todo_public_ver_1.jpg)

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
#�v���_�E���ɕ\������閼�O=TODO�t�@�C�����i�[���Ă���t�H���_�̐�΃p�X
#��
#F:\Document\800_IT���Ȋw�K\09_python\51_Qiita�Ƃ����t�H���_��TODO�t�@�C�����i�[����ꍇ
qiita=F:\Document\800_IT���Ȋw�K\09_python\51_Qiita

[File_names]
#TODO���X�g�ꗗ�ɕ\���������t�@�C�����B���C���h�J�[�h(*)���g�p�ł��܂��B
#��

#�擪��todo�Ƃ��������񂪂���t�@�C��
todo=todo*

#�g���q��py�̃t�@�C��
python=*.py

[Importance_color]
#�d�v�x��\�����߂Ƀt�@�C�����Ŏg�p���镶����ƑΉ�����F
#default�͏d�v�x�̕����񂪓����Ă��Ȃ��t�@�C���ɑ΂��Ďg�p�����F�ł��B
#�F��red��blue�Ȃǂ̕�����Ŏw�肵�܂��B
default=white
A=red
B=yellow
C=green

[Meta_data]
#���^�f�[�^�Ƃ��Ďg�p����t�@�C�����̕�����̈ʒu�ƃ��^�f�[�^�̃L�[��
#TODO�t�@�C���̃t�@�C�����̂���[#metadata]�̂悤�ɁA[]�ň͂܂ꂽ#�Ŏn�܂镶�������^�f�[�^�Ƃ��ĔF�����܂��B
# example: [#2020/09/01][#�@�\�ǉ�]example.txt�Ƃ���Ί���:2020/09/01 �J�e�S��:�@�\�ǉ��ƂȂ�܂��B
#          [#][#�@�\�ǉ�]example.txt�Ƃ���΃J�e�S��:�@�\�ǉ��ƂȂ�܂��i#�����Ȃ����ߊ����͖��������j�B
1=����
2=�J�e�S��
```



**config.ini**��ҏW����ۂ̒��ӓ_�ɂȂ�܂��B

- **Dir_names**�ɂ͕����̃t�H���_�����L�ڂł��܂��B
- **File_names**�ɂ͕����̃t�@�C�������L�ڂł��܂��B
- �t�@�C�������L�ڂ���ꍇ�̓��C���h�J�[�h�i*�j���g�p�ł��܂��B
- �t�@�C�����𕡐��L�ڂ����ꍇ��**or**�̌����ɂȂ�܂��B
- **Importance_color**�Ŏw�肵���F�ɂ���ꍇ�́A�t�@�C������**[������]**�������܂��i��F**A=red**�Ƃ����ꍇ�́A**[A]hogehoge**�Ƃ����t�@�C�����ɂ���j�B

**��1  �L�ڂ����t�H���_���z���ɑ�ʂ̃t�H���_�A�t�@�C��������ꍇ�A��������̂Ɏ��Ԃ�������ꍇ������܂��B**
 **�ɒ[�Șb�ł����t�H���_����C:\�ƋL�ڂ���ƁATODO���X�g��\������܂łɂ��Ȃ�̎��Ԃ�v���܂��B**

**��2  TODO�t�@�C���̕����R�[�h��UTF-8�ɂ��Ă��������B�ڍ׉�ʂ��\������܂���B**

### ���s���@

> python display.py

## �����ꗗ

[Simple Todo �Ŏ�������������](./doc/SimpleTodo�Ŏ�������������.md)

