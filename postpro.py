'''
つくられた一時ファイルを削除する
'''

import os
import glob

def del_files(del_list):
    if del_list:
        for i in del_list:
            os.remove(i)
            