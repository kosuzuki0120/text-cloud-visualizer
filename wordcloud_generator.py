'''
感情値分析した画像を作成する
'''

import random
import colorsys
import codecs
import pandas as pd
from wordcloud import WordCloud

def calc_rgb(n):
    return int(min(n, 1) * 256)

def color_func(word, font_size, position, orientation, random_state, font_path):
    """
    単語の文字色を決定する

    """

    pn_df = pd.read_csv('pn_table_ja.dic', sep=':', encoding='shift-jis', names=('Word','Reading','POS','PN'))
    pn_dict = dict(zip(list(pn_df['Word']), list(pn_df['PN'])))

    word = word.rstrip('だ')  #「だ」を除くことで名詞として認識
    if word in pn_dict:
        pn = float(pn_dict[word])
    else:
        pn = 0.00  #PN Tableに単語が無かった場合

    if pn > 0:
        h, s, v = 0.45 - (pn / 2.5), 1.0, 0.7
    elif pn < 0:
        h, s, v = 0.45 - (pn / 6.0), 1.0, 0.7
    else:
        h, s, v = 0.45, 1.0, 0.7

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    font_color = tuple(map(calc_rgb, [r, g, b]))
    
    return font_color

def create_wordcloud(csv_list, pngname):
    """
    CSV ファイルを読み込んで画像を出力する

    """

    words = []

    try:
        for csv in csv_list:
            csvopen = codecs.open(csv, 'r', encoding="utf8")
            csvread = csvopen.readlines()
            csvopen.close()
            
            for line in csvread:
                words.append(line.rstrip())

        words = random.sample(words, len(words)) #単語同士が繋がる場合があるのでシャッフル

        #wordcloudオブジェクトの作成
        font_path = '/usr/share/fonts/truetype/migmix/migmix-1p-regular.ttf'  #フォントの指定
        stop_words = ['無い'] #'無い'を除外
        wordcloud = WordCloud(background_color='white', font_path=font_path, width=1600, height=1066,
                    stopwords=set(stop_words), color_func=color_func, regexp=r'\w+').generate(' '.join(words))

        print('出力しています...');

        #wordcloudファイル出力
        wordcloud.to_file('result/' + pngname + '.png')

    except Exception as e:
        print(f'error : {e}')
