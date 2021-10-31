import os
import fnmatch
#root:ディレクトリ名
#patterns:unixのシェル形式のワイルドカードへ対応。ファイル名のパターン
#yeild_folders:サブディレクトリ配下のファイルを読み込むかどうか。

def get_all_files(root, patterns = "*", single_level=False, yeild_folders=False):
#split:";"でパターンを複数指定できる。;はパターンに入れられない。
    patterns = patterns.split(";")

#os.walkで指定したディレクトリ以下のディレクトリパス名、ディレクトリ名、ファイル名を渡す。
    for path, subdirs, files in os.walk(root):
        if yeild_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                #fnmatchはnameがpatternに一致する場合、Trueを返す。
                if fnmatch.fnmatch(name, pattern) and not ("[完了]" in name):
                    yield os.path.join(path, name)
                    break
        if single_level:
            break
