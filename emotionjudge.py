from collections import defaultdict
import os
import re
import jieba
import codecs
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import xlrd,xlwt
from xlutils.copy import copy
from test import sent2word
from txt2_list import txt2_list

# jieba.load_userdict(r'词库\正面情绪.txt')
# jieba.load_userdict(r'词库\负面情绪.txt')
# jieba.load_userdict(r'词库\通用词语.txt')
"""
1. 文本切割
"""


#读取情绪词库
def emotionjg(data):
    posff = open(r'沐浴露词库\沐浴露词库\专业\沐浴露正面.txt','r',encoding='utf-8',errors='ignore')

    poswords = []
    poslines = posff.readlines()
    for i in range(0,len(poslines)):
        posword = poslines[i].strip("\n")
        poswords.append(posword)
    #添加总体正面词库
    postotal = open(r'沐浴露词库\沐浴露词库\通用\正面情绪.txt','r',encoding='utf-8',errors='ignore')    
    postlines = postotal.readlines()
    for i in range(0,len(postlines)):
        posword = postlines[i].strip("\n")
        poswords.append(posword)
    #print(poswords)
    negff = open(r'沐浴露词库\沐浴露词库\专业\沐浴露负面.txt','r',encoding='utf-8',errors='ignore')
    negwords = []
    neglines = negff.readlines()
    for i in range(0,len(neglines)):
        negword = neglines[i].strip("\n")
        negwords.append(negword)
    #print(data)
    #print(negwords) 
    negtotal = open(r'沐浴露词库\沐浴露词库\通用\负面情绪.txt','r',encoding='utf-8',errors='ignore')
    negtlines = negtotal.readlines()
    for i in range(0,len(negtlines)):
        negword = negtlines[i].strip("\n")
        negwords.append(negword)
    #print(negwords) 
    wordlists = list(set(sent2word(data).split(' ')))#.remove('')
    #print(wordlists)
    PorN = 0

    for j in range(len(wordlists)):
        #ws.write(i,j+4,wordlists[j])
        if wordlists[j] in negwords:
            PorN-=1
        elif wordlists[j] in poswords:
            PorN+=1
            #print(wordlists[j],PorN)
    return PorN
    #添加总体负面词库 

# print(negwords)
# print(commentline)
def emotionjg_no(data,files,db = 1):
    # posff = open(r'沐浴露前缀否定\专业\后缀正面.txt','r',encoding='utf-8',errors='ignore')

    # poswords = []
    # poslines = posff.readlines()
    # for i in range(0,len(poslines)):
    #     posword = poslines[i].strip("\n")
    #     poswords.append(posword)
    
    # negff = open(r'沐浴露前缀否定\专业\后缀负面.txt','r',encoding='utf-8',errors='ignore')
    # negwords = []
    # neglines = negff.readlines()
    # for i in range(0,len(neglines)):
    #     negword = neglines[i].strip("\n")
    #     negwords.append(negword)
    poswords = []
    negwords = []
    poswords = txt2_list(r'%s\通用\后缀正面.txt'%files,poswords)
    negwords =txt2_list(r'%s\通用\后缀负面.txt'%files,negwords)
    poswords = txt2_list(r'%s\专业\后缀正面.txt'%files,poswords)
    negwords =txt2_list(r'%s\专业\后缀负面.txt'%files,negwords)
    l1 = sent2word(data,files).split(' ')
    wordlists = []
    for i in l1:
        if i not in wordlists:
            wordlists.append(i)
    
    print(wordlists)
    nolist=[]
    nolist = txt2_list(r'%s\通用\前缀负面.txt'%files,nolist)
    nolist = txt2_list(r'%s\专业\前缀负面.txt'%files,nolist)
    PorN = 0
    print(wordlists)
    for j in range(len(wordlists)):
        #ws.write(i,j+4,wordlists[j])
        
        if wordlists[j] in negwords:
            #print(j)
            PorNum = 0
            qq = j
            print('-'+wordlists[j])
            PorNum-=1
            print(PorNum)
            for q in range(qq):
                #print(q)
                #print(wordlists[q])
                if wordlists[q] in nolist:
                    print('否定'+wordlists[q])
                    PorNum = PorNum*(-1)
                    print(PorNum)
            PorN+=PorNum
        elif wordlists[j] in poswords:
            qq = j
            PorNum = 0
            print('+'+wordlists[j])
            PorNum+=(1*db)
            print(PorNum)
            for q in range(qq):
                if wordlists[q] in nolist:
                    print('否定'+wordlists[q])
                    PorNum = PorNum*(-1)
            PorN+=PorNum
                    # print(PorNum)          
            #print(wordlists[j],PorNum)
        #if wordlists[j] in nolist:
    print(PorN)        
    return PorN
#print(emotionjg('不好，你妹的，一点都不好用'))
if __name__ == '__main__':
    sent = '挺好的没有假滑'
    spsent = re.split('[，。,.；;!?！？ ...~~、…]',sent)
    for i in spsent:
        print(emotionjg_no(i,'牙膏'))
#     #main()
#     commenttext = '雅诗兰黛素颜霜好用'
#     print(negwords)
#     # resultff = open(r'宽带\上海电信\emonum.txt','w')
#     data = xlrd.open_workbook(r'C:\Users\stacy\Desktop\评论\六神汉方清肌沐浴露香氛沐浴乳.xlsx') # 打开xls文件
#     #分词并填到后面的表格中
#     #判断情绪正负态
#     wb = copy(data)
#     ws = wb.get_sheet(2)
#     table = data.sheets()[2] # 打开第一张表
#     nrows = table.nrows # 获取表的行数
#     for i in range(nrows): # 循环逐行打印
#         if i == 0: # 跳过第一行
#             continue
#         if type(table.row_values(i)[0])!= float:
#             text = sent2word(table.row_values(i)[0])
#             print(text)
#             listtext = text.split(' ')
#         PorN = 0
#         for j in range(1,len(listtext)-1):
#             #ws.write(i,j+4,listtext[j])
#             if listtext[j] in negwords:
#                 PorN-=1
#             elif listtext[j] in poswords:
#                 PorN+=1
#         ws.write(i,1,str(PorN))
#         #resultff.write(str(i)+' ' +str(PorN)+'\n')
#         print(i,PorN)
#     wb.save(r'C:\Users\stacy\Desktop\评论\六神汉方.xls')

# resultff.close()
# print(text)
# print(type(text))

