'''
形態素解析する
'''

import os
import glob
import subprocess
import codecs

def juman_exec(review_list):
    """
    テキスト読み込んで Juman の結果をつくる

    """

    for review in review_list:
        try:
            with open(review, 'r') as f:
                text = f.read()
                
            juman_args = ['juman']
            juman_proc = subprocess.Popen(juman_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            juman_result, _ = juman_proc.communicate(text.encode('utf-8'))
            with open(os.path.join('juman', os.path.basename(review)), 'wb') as f:
                f.write(juman_result)

        except Exception as e:
            print(f'error : {e}')

def result2csv(juman_list):
    """
    Juman の結果から代表表記を取り出して CSV にかく

    """

    for juman_file in juman_list:
        try:
            juman_read = codecs.open(juman_file, 'r', 'utf8')
            juman_data = juman_read.readlines()
            juman_read.close()
            csv_write = codecs.open('juman/'+os.path.basename(juman_file)[:-4] + '.csv', 'w', 'utf8')

            #juman の結果から代表表記をとりだす
            for line in juman_data:
                if line.find(' 形容詞 ') >= 0 and line.find('代表表記:') >= 0:
                    line = line.split('代表表記:')[1]
                    line = line.split('/')[0]
                    csv_write.write(line+'\n')
            csv_write.close()

        except Exception as e:
            print(f'error : {e}')
            