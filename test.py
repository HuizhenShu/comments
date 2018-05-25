from collections import defaultdict
import os
import re
import jieba
#import codecs
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.dates as mdate
from pylab import *  
import xlrd
from txt2_list import txt2_list




#jieba.load_userdict(r'沐浴露词库\沐浴露词库\专业\沐浴露负面.txt')
#jieba.load_userdict(r'沐浴露词库\沐浴露词库\通用\通用词语.txt')
# jieba.load_userdict(r'词库\彩妆.txt')
# jieba.load_userdict(r'词库\母婴.txt')
# jieba.load_userdict(r'词库\头发.txt')
# jieba.load_userdict(r'词库\护肤.txt')

# jieba.load_userdict(r'\词库\否定词.txt')
# jieba.load_userdict(r'\词库\BB霜负面.txt')
# jieba.load_userdict(r'\词库\BB霜正面.txt')
# jieba.load_userdict(r'\词库\品牌.txt')
# jieba.load_userdict(r'\词库\词库.txt')
from collections import Counter  
import nltk
import jieba.analyse
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体  
  
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题  
abel_mask = np.array(Image.open(r"图片/粉饼.jpg"))

"""
1. 文本切割
"""

def sent2word(sentence,files):
	"""
	Segment a sentence to words
	Delete stopwords
	"""
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
	segList1 = jieba.cut(sentence)
	#print(segList1)
	text = " ".join(segList1)
	segResult = []
	for w in segList:
		segResult.append(w)
	print(segResult)
	ff = open(r'牙膏\通用\中文停用词表.txt','r',encoding='utf-8')
	stopwords = []
	lines = ff.readlines()
	for i in range(0,len(lines)):
		stopword = lines[i].strip("\n")
		stopwords.append(stopword)
	#print(stopwords)
	newSent = []
	for word in segResult:
		if word in stopwords:
			# print "stopword: %s" % word
			continue
		else:
			newSent.append(word)

	# return newSent
	# print(segResult)
	print(newSent)
	cleantext = ''
	for i in newSent:
		cleantext = cleantext+' '+i
	#print(cleantext.replace('\ufeff','').replace('\ue600','').replace('\ue601','').replace('\xeb',''))
	#print(cleantext)
	return cleantext
def jieba_keywords(news):
    keywords = jieba.analyse.extract_tags(news, 1000, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    #print (keywords)
if __name__ == '__main__':
	sent2word('非常好，易冲洗，洗完身体不会假滑')
	# txte = open('敏感肌.txt','rb').readlines()#从文本中获取语料
	# #print(txte)
	# textlsit = []
	# for x in range(len(txte)):
	# 	textlsit.append(txte[x].decode('utf-8'))
	# print(textlsit)
	# jieba_keywords(textlsit[0])
	# poswords = []
 #    #添加总体正面词库
	# postotal = open(r'E:\工作文件\文本分析\2017.12.18化妆品词库\分词词库\正面情绪.txt','r',encoding='utf-8',errors='ignore')    
	# postlines = postotal.readlines()
	# for i in range(0,len(postlines)):
	# 	posword = postlines[i].strip("\n")
	# 	poswords.append(posword)
 #    #print(poswords)
 #    #添加总体负面词库
	# negwords = []
	# negtotal = open(r'E:\工作文件\文本分析\2017.12.18化妆品词库\分词词库\负面情绪.txt','r',encoding='utf-8',errors='ignore')
	# negtlines = negtotal.readlines()
	# for i in range(0,len(negtlines)):
	# 	negword = negtlines[i].strip("\n")
	# 	negwords.append(negword)

	#将分词结果写入
	# fenciresult = open(r'文本挖掘test/zhihu.csv','w')#,encoding='utf8', newline=''
	# #从txt文本读取评论数据
	# comment = open(r'E:\工作文件\文本分析\文本挖掘test\敏感肌知乎.csv','r',encoding='utf-8',errors='ignore')
	# # #comment =  xlrd.open_workbook(r'文本挖掘test/问题.xlsx')#(),encoding=
 #    # for w in words:

 #    # sentence = strdecode(sentence)'utf-8',errors='ignore'
	# # # table = comment.sheets()[0] 
	# # # nrows = table.nrows
	# # # ncols = table.ncols
	# commentline = comment.readlines()
	# # #print(commentline)
	# commenttext = ''
	# # # print (len(comment))
	# # # print (type(comment))
	# # #print (nrows)
	# # #print (table.row_values(7000))
	# # def float(n):
	# # 	try:
	# # 		n.strip("\n").strip("\t")
	# # 		return False
	# # 	except:
	# # 		return True
	# # # for i in range(nrows):
	# # # 	#print (table.row_values(i))
	# # # 	if float(table.row_values(i)):
	# # # 		item = str(table.row_values(i)[0])
	# # # 	else:
	# # # 		item = str(table.row_values(i)[0].strip("\n").strip("\t"))
	# # # 	line = sent2word(item).replace('\ufeff','').replace('\ue600','').replace('\ue601','').replace('\xeb','').replace('\u20ac','')
	# # # 	fenciresult.write(line)
	# # # 	print(str(i)+':'+line)
	# # # 	ftt = item.strip("\n").strip("\t").replace('\ufeff','').replace('\ue600','').replace('\ue601','').replace('\xeb','').replace('\xfb','')
	# # # 	#print(i)
	# # # 	commenttext = commenttext+ftt
	# num = 0
	# for i in commentline:
	# 	ftt = i.strip("\n").strip("\t").encode('GBK', 'ignore').decode('GBK', 'ignore');#\
	# 	# .replace('\ufeff','').replace('\u2038','').replace('\ue601','').replace('\xb4','').replace('\xfb','').replace('\u2022','').\
	# 	# replace('\uff65','').replace('\u0306','').replace('\u0e34','').replace('\u053e','').replace('\xaf','').replace('\uff9f','').replace('\u2764','').replace('\xf4','').replace('\ufe0f','').\
	# 	# replace('\u301c','').replace('\u2028','').replace('\u0e51','').replace('\u2207','').replace('\u2728','')
	# 	#print(sent2word(ftt),num)
	# 	num+=1
	# 	try:
	# 		pass
	# 		#fenciresult.write(sent2word(ftt))
	# 	except Exception as e:
	# 		print(e)
	# 	commenttext = commenttext+ftt
	# #fenciresult.close()
	# #使用pandas从excel读取评论数据
	# file = 'E:\工作文件\文本分析\知乎评论.xlsx'
	# df = pd.read_excel(file)
	# print(df)
	# print(commenttext)

	#text = sent2word(commenttext)
	# #print(text)
	#word_lst = text.split(' ')#list
	# word_lst=[]
	# text_list = []
	# txt2_list(r'敏感肌.txt',text_list)
	# for i in range(len(text_list)):
	# 	print(text_list[i].split(' '))
	# 	word_lst = word_lst+text_list[i].split(' ')
	# # wordfre = nltk.FreqDist(word_lst)
	# # #print (word_lst)

	# biword = nltk.FreqDist(list(nltk.bigrams(word_lst)))
	# print (biword.most_common(500))
	# print(wordfre)
	# # emotext = open(r'词性.csv','w',encoding='utf-8',errors='ignore')

	# #词频
	# # textfre = open(r'词频.csv','w',encoding='utf-8',errors='ignore')
	# # print(wordfre.most_common(1000))
	# # # # print(len(wordfre.most_common()))
	# # for i in wordfre.most_common(len(wordfre.most_common())):
	# # 	textfre.write(str(i[0])+':'+str(i[1])+'\n')


	# # 	emotext.write(str(i[0])+str(i[1]))
	# # 	if i[0] in poswords:
	# # 		print('zhengm')
	# # 		emotext.write(','+'正面')
	# # 	if i[0] in negwords:
	# # 		emotext.write(','+'负面')	
	# # 	emotext.write('\n')
	# # emotext.close()	
	# #print(len(wordfre))
	# # fretext = open(r'Q4__open词频.txt','w',encoding='utf-8',errors='ignore')
	# # for i in wordfre.most_common(len(wordfre)):
	# # 	fretext.write(i[0]+'\t'+str(i[1])+'\n')
	# #print (wordfre.most_common(len(wordfre)))

	# #print('hh')
	# commomlist = []
	# for i in range(20):
	# 	commomlist.append(nltk.FreqDist(word_lst).most_common(20)[i][0])###获取top词汇组成的list
	# word_text = nltk.Text(word_lst)#nltk中使用的文本形式
	# #print(word_text)
	# # change = word_text.dispersion_plot(commomlist)




	# # print(wordfre)
	# # stopwords = ('推荐','一定','真的','不是','人','再','最','皮肤','产品','使用','买','不','好','觉得','特别','用','\t','\n')

	# # #创建词云
	# # wordcloud = WordCloud(font_path=r"C:\Windows\Fonts\simkai.ttf",mask=abel_mask,stopwords=stopwords,random_state = 30, max_words = 1000, width=1500, height=1000,background_color="white",min_font_size = 5).generate_from_frequencies(wordfre)#.generate_from_text(text)#
	# # image_colors = ImageColorGenerator(abel_mask)#
	# # #wordcloud.recolor(color_func = image_colors)

	# # fig = plt.imshow(wordcloud)

	# # #plt.title('大家的烦恼')
	# # plt.axis("off")
	# # plt.savefig('知乎男士护肤.jpg',dpi=100)
	# # plt.show()



