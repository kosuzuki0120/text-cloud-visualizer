'''
アプリケーションを起動する
'''

import glob
import juman
import wordcloud_generator
import postpro

def main():
    print('出力結果のファイル名を決めてください')
    pngname = input('ファイル名:')

    review_list = glob.glob('review/*.txt')
    juman.juman_exec(review_list)

    juman_list = glob.glob('juman/*.txt')
    juman.result2csv(juman_list)

    csv_list = glob.glob('juman/*.csv')
    wordcloud_generator.create_wordcloud(csv_list, pngname)

    del_list = juman_list + csv_list
    postpro.del_files(del_list)
    
if __name__ == '__main__':
    main()
