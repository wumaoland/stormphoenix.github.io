def cut_txt(old_file):
    import jieba
    global cut_file
    cut_file = old_file + '_cut.txt'

    try:
        fi = open(old_file, 'r', encoding='utf-8')
    except BaseException as e:
        print(Exception, ":", e)

    text = fi.read()
    new_text = jieba.cut(text, cut_all=False)
    str_out = ' '.join(new_text).replace('，', '').replace('。', '').replace('？', '').replace('！', '') \
        .replace('“', '').replace('”', '').replace('：', '').replace('…', '').replace('（', '').replace('）', '') \
        .replace('—', '').replace('《', '').replace('》', '').replace('、', '').replace('‘', '') \
        .replace('’', '')     # 去掉标点符号
    fo = open(cut_file, 'w', encoding='utf-8')
    fo.write(str_out)
