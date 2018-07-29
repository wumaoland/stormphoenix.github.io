from gensim.models import word2vec
import os
import gensim

# if not os.path.exists(cut_file):    # 判断文件是否存在，参考：https://www.cnblogs.com/jhao/p/7243043.html
cut_txt('倚天屠龙记.txt')  # 须注意文件必须先另存为utf-8编码格式

save_model_name = '倚天屠龙记.model'
if not os.path.exists(save_model_name):     # 判断文件是否存在
    model_train(cut_file, save_model_name)
else:
    print('此训练模型已经存在，不用再次训练')

# 加载已训练好的模型
model_1 = word2vec.Word2Vec.load(save_model_name)
# 计算两个词的相似度/相关程度
y1 = model_1.similarity("赵敏", "韦一笑")
print(u"赵敏和韦一笑的相似度为：", y1)
print("-------------------------------\n")

# 计算某个词的相关词列表
y2 = model_1.most_similar("张三丰", topn=10)  # 10个最相关的
print(u"和张三丰最相关的词有：\n")
for item in y2:
    print(item[0], item[1])
print("-------------------------------\n")
