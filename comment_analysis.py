import pandas as pd
from pandas import DataFrame,Series
import numpy as np
import os
import jieba
from collections import Counter
import nltk
from collections import defaultdict
import re
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.dates as mdate
from pylab import *
from txt2_list import txt2_list

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
#将不同sheet合并
def concat_data(fname,pro_list):
    df = pd.read_excel(fname,pro_list[0])
    df['pro'] = pro_list[0]
    for i in range(1,len(pro_list)):
        temp = pd.read_excel(fname,pro_list[i])
        temp['pro'] = pro_list[i]
        df = pd.concat([df,temp],ignore_index=True)
    return df

def communilate(df,fname,dataname,files):
    attri_list = ['肤感', '气味', '质地', '效果', '外观', '价格', '包装']
    attri_list2 = attri_list + ['总体']
    df[attri_list2] = np.clip(df[attri_list2], -1, 1)
    attriLen_list = [x + '长度' for x in attri_list]
    df[attriLen_list] = np.clip(df[attriLen_list], 0, 1)
    rst1 = df.pivot_table(index='pro', columns='总体', values='评论', aggfunc=len)
    rst1_sum = df.pivot_table(index='pro', columns='总体', values='评论', aggfunc=len)
    rst1 = rst1.div(rst1.sum(axis=1), axis=0)
    rst1.rename(columns={-1: '负面', 0: '中性', 1: '正面'}, inplace=True)
    rst1_sum.rename(columns={-1: '负面评论条数', 0: '中性评论条数', 1: '正面评论条数'}, inplace=True)
    rst1['美誉度'] = (rst1['正面'] * 2 + rst1['中性']) / (rst1['正面'] * 2 + rst1['中性'] + rst1['负面'] * 3)
    rst1 = rst1.sort_values('美誉度', ascending=False)
    rst1['评论数'] = df.groupby('pro')['评论'].count()
    rst1 = pd.concat([rst1, rst1_sum], axis=1, join_axes=[rst1.index])
    pro_list = list(rst1.index.values)

    grp = df[attriLen_list].groupby(df['pro'])
    rst2 = grp.apply(lambda x: x.sum() / x.shape[0])
    rst2.columns = [x.replace('长度', '') for x in rst2.columns]
    attri_sort = attri_list
    rst2 = rst2.reindex(columns=attri_sort)
    rst2 = rst2.reindex(index=pro_list)

    rst3_list = [''] * len(attri_list)
    for i in range(len(attri_list)):
        attri = attri_list[i]
        dfsp = df[['pro', attri, attri + '长度']]
        dfsp = dfsp[dfsp[attri + '长度'] == 1]
        rst3_list[i] = dfsp.pivot_table(index='pro', columns=attri, values=attri + '长度', aggfunc=len)
        rst3_sum = dfsp.pivot_table(index='pro', columns=attri, values=attri + '长度', aggfunc=len)
        rst3_list[i] = rst3_list[i].div(rst3_list[i].sum(axis=1), axis=0)
        rst3_sum.rename(columns={-1: '负面评论条数', 0: '中性评论条数', 1: '正面评论条数'}, inplace=True)
        rst3_list[i].rename(columns={-1: '负评率', 0: '中性评率', 1: '正面评率'}, inplace=True)
        rst3_list[i] = pd.concat([rst3_list[i], rst3_sum], axis=1, join_axes=[rst3_list[i].index])
        rst3_list[i]['非负评价率'] = rst3_list[i]['正面评率'] + rst3_list[i]['中性评率']
    rst = pd.concat(rst3_list, keys=attri_list)
    rst['总数'] = 1
    cols = ['正面评论条数','中性评论条数','负面评论条数','正面评率','中性评率','负评率','总数','非负评价率']
    rst = rst[cols]
    rst3 = rst.unstack()['非负评价率']
    rst3 = rst3.reindex(columns=pro_list)
    if os.path.isfile(fname):
        os.remove(fname)
    xw = pd.ExcelWriter(fname)
    rst1.to_excel(xw, '整体-情绪')
    rst2.to_excel(xw, '属性-关注度')
    rst3.to_excel(xw, '属性-情绪')
    df_wordfre1 = pd.DataFrame(columns=['词频'],index=pro_list)
    df_wordfre2 = pd.DataFrame(columns=['词频'], index=pro_list)
    for name in pro_list:
        writer = rst.unstack().swaplevel(1, 0, axis=1).sort_index(axis=1)[name]
        writer = writer[cols]
        writer.to_excel(xw, '属性-非负评价率-'+name)
        df_wordfre1.loc[name,'词频'] = fun(dataname,name,files)[0]
        df_wordfre2.loc[name, '词频'] = fun(dataname, name,files)[1]
    df_wordfre1.to_excel(xw,'负面评价词频')
    df_wordfre2.to_excel(xw, '正面评价词频')
    xw.save()

def sent2word(sentence,files):
    jieba.load_userdict(r'%s\通用\通用词语.txt'%files)
    jieba.load_userdict(r'%s\通用\网络流行语词库.txt'%files)
    jieba.load_userdict(r'%s\通用\后缀负面.txt'%files)
    jieba.load_userdict(r'%s\专业\后缀负面.txt'%files)
    jieba.load_userdict(r'%s\通用\前缀负面.txt'%files)
    jieba.load_userdict(r'%s\专业\前缀负面.txt'%files)
    jieba.load_userdict(r'%s\通用\后缀正面.txt'%files)
    jieba.load_userdict(r'%s\专业\后缀正面.txt'%files)
    jieba.load_userdict(r'%s\通用\前缀正面.txt'%files)
    jieba.load_userdict(r'%s\专业\前缀正面.txt'%files)
    jieba.load_userdict(r'%s\专业\属性\气味.txt'%files)
    jieba.load_userdict(r'%s\专业\属性\质地.txt'%files)
    jieba.load_userdict(r'%s\专业\属性\肤感.txt'%files)
    jieba.load_userdict(r'%s\专业\属性\效果.txt'%files)
    jieba.load_userdict(r'%s\专业\属性\外观.txt'%files)
    jieba.load_userdict(r'%s\品牌词库.txt'%files)
    jieba.load_userdict(r'词库\网络流行语词库.txt')
    segList = jieba.cut(sentence)
    segResult = []
    for w in segList:
        segResult.append(w)
    ff = open('词库\中文停用词表.txt','r',encoding='utf-8')
    stopwords = []
    lines = ff.readlines()
    for i in range(0,len(lines)):
        stopword = lines[i].strip("\n")
        stopwords.append(stopword)
    newSent = []
    for word in segResult:
        if word in stopwords:
            continue
        else:
            newSent.append(word)
    cleantext = ''
    for i in newSent:
        cleantext = cleantext+' '+i
    return cleantext
def float(n):
    try:
        n.strip("\n").strip("\t")
        return False
    except:
        return True
def fun1(comment,files):
    commentline = comment['评论'].values
    commenttext = ''
    for i in commentline:
        if not float(i):
            ftt = i.strip("\n").strip("\t").replace('\ufeff', '').replace('\ue600', '').replace('\ue601', '').replace(
                '\xeb', '').replace('\xfb', '').replace('\u20ac', '')
        commenttext = commenttext + str(ftt)
    text = sent2word(commenttext,files)
    # print(text)
    word_lst = text.split(' ')  # list
    wordfre = nltk.FreqDist(word_lst)
    return wordfre

def fun(dataname,sheetnames,files):
    comment = pd.read_excel('./'+dataname,sheetname=sheetnames)
    comment1 = comment[comment['总体']<0]
    comment2 = comment[comment['总体']>0]
    wordfre = fun1(comment,files)
    wordfre1 = fun1(comment1,files)
    wordfre2 = fun1(comment2,files)
    #wordfre = nltk.FreqDist(list(nltk.bigrams(word_lst)))
    word_fre = wordfre1.most_common(100)
    word_fre1 = wordfre2.most_common(100)
    # if os.path.isfile(filepath+'词云图/'+sheetnames+'.csv'):
    #     os.remove(filepath+'词云图/'+sheetnames+'.csv')
    # with open(filepath+'词云图/'+sheetnames+'.csv','w',encoding='utf-8') as f:
    #     for word in wordfre.most_common():
    #         f.write(str(word[0])+':'+ str(word[1]) +'\n')
    # commomlist = []
    # for i in range(20):
    #     commomlist.append(nltk.FreqDist(word_lst).most_common(20)[i][0])  ###获取top词汇组成的list
    # word_text = nltk.Text(word_lst)  # nltk中使用的文本形式
    #print(wordfre.most_common())

    # 创建词云
    stopwords = ('推荐', '一定', '真的', '不是', '人', '再', '最', '皮肤', '产品', '使用', '买', '不', '好', '觉得', '特别', '用', '\t', '\n')
    abel_mask = np.array(Image.open('E:\工作文件\文本分析\图片\\'+"粉饼.jpg"))
    wordcloud = WordCloud(font_path=r"C:\Windows\Fonts\simkai.ttf", mask=abel_mask, stopwords=stopwords,
                          random_state=30, max_words=1000, width=3500, height=300, background_color="white",
                          min_font_size=5).generate_from_frequencies(wordfre)  # .generate_from_text(text)#
    image_colors = ImageColorGenerator(abel_mask)  #
    fig = plt.imshow(wordcloud)
    plt.axis("off")
    if os.path.isfile('./'+ sheetnames +'.jpg'):
        os.remove('./' + sheetnames +'.jpg')
    plt.savefig('沐浴露/'+'词云图/'+ sheetnames +'.jpg', dpi=300)
    #plt.show()
    return word_fre,word_fre1



if __name__ == '__main__':
    pro_list = []
    #pro_list = txt2_list(r'沐浴露\品牌词库.txt',pro_list)
    pro_list = ['滴露薄荷冰爽沐浴露','多芬衡悦水润沐浴乳','力士爽肤闪亮冰爽沐浴露','六神冰凉超爽沐浴乳','舒肤佳柠檬清新沐浴露','资生堂可悠然美肌沐浴露']
    #['蜕唤美小黑裙沐浴露','COCOVEL香体沐浴露','KJU木槿花香济之州宠肤沐浴露','东方宝石水润嫩肤香氛沐浴露','蔻斯汀樱花花瓣沐浴露沐浴液','力士精油香氛沐浴露幽莲魅肤']
    #
    #
    # with open('沐浴露\品牌词库.txt','r') as f:
    #     for line in f.readlines():
    #         pro_list.append(line.strip())
    communilate(concat_data('沐浴露/'+'整体数据2.xlsx',pro_list),'沐浴露/'+'数据导出2.xlsx','沐浴露/整体数据2.xlsx','沐浴露')
