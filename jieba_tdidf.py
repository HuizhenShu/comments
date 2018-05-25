
import pandas
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from txt2_list import txt2_list
#jieba.load_userdict("namedict.txt")

# jieba.load_userdict(r'洗面奶词库\正面情绪.txt')
# jieba.load_userdict(r'洗面奶词库\负面情绪.txt')
# jieba.load_userdict(r'洗面奶词库\洗面奶正面.txt')
# jieba.load_userdict(r'洗面奶词库\洗面奶负面.txt')
# jieba.load_userdict(r'洗面奶词库\通用词语.txt')
# jieba.load_userdict(r'词库\彩妆.txt')
# jieba.load_userdict(r'词库\母婴.txt')
# jieba.load_userdict(r'词库\头发.txt')
# jieba.load_userdict(r'词库\护肤.txt')
# jieba.load_userdict(r'词库\网络流行语词库.txt')
# 设置相关的文件路径
bg_image_path = r"图片/粉饼.jpg"
text_path = '文本挖掘test/敏感肌知乎.txt'
excel_path = '沐浴露/整体数据1.xlsx'
font_path = r"C:\Windows\Fonts\simkai.ttf"
stopwords_path = '沐浴露\通用\中文停用词表.txt'


def clean_using_stopword(text,files):
    """
    去除停顿词，利用常见停顿词表+自建词库
    :param text:
    :return:
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
    stopwords_path = '牙膏\通用\中文停用词表.txt'
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)
    #with open(stopwords_path) as f_stop:
    f_stop_seg_list = []
    f_stop_seg_list = txt2_list(stopwords_path,f_stop_seg_list)
    #f_stop_text = unicode(f_stop_text, 'utf-8')
    print(f_stop_seg_list)
    #f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):  # 去除停顿词，生成新文档
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    print (''.join(mywordlist))
    return ''.join(mywordlist)


def preprocessing(filepath,files,product,attr):
    """
    文本预处理
    :return:
    """
    #with open(text_path) as f:
    # content = readtxtline(text_path)
    # print(content)
    content = readexcel(filepath)[product][attr]
    return clean_using_stopword(content,files)
    return content


def extract_keywords(filepath,files,product,attr):
    """
    利用jieba来进行中文分词。
    analyse.extract_tags采用TF-IDF算法进行关键词的提取。
    :return:
    """
    # 抽取1000个关键词，带权重，后面需要根据权重来生成词云
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
    allow_pos = ('nr',) # 词性
    tags = jieba.analyse.extract_tags(preprocessing(filepath,files,product,attr), 1500, withWeight=True)#,allowPOS='a'
    keywords = dict()
    for i in tags:
        print("%s---%f" % (i[0], i[1]))
        keywords[i[0]] = i[1]
    #print (keywords)
    return keywords



def draw_wordcloud(filepath,files,product,attr):
    """
    生成词云。1.配置WordCloud。2.plt进行显示
    :return:
    """
    import os
    back_coloring = plt.imread(bg_image_path)  # 设置背景图片
    # 设置词云属性
    wc = WordCloud(font_path=font_path,  # 设置字体
                   background_color="white",  # 背景颜色
                   max_words=2000,  # 词云显示的最大词数
                   mask=back_coloring,  # 设置背景图片
                   )

    # 根据频率生成词云
    wc.generate_from_frequencies(extract_keywords(filepath,files,product,attr))
    # 显示图片
    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
    #plt.show()
    # 保存到本地
    if os.path.isdir('沐浴露/词云图/%s'%product):
       pass
    else:
       os.mkdir('沐浴露/词云图/%s'%product)
    plt.savefig("沐浴露/词云图/%s/%s.jpg"%(product,attr), dpi=300)
def file_encoding(file_path):  
    """ 
    获取文件编码类型\n 
    :param file_path: 文件路径\n 
    :return: \n 
    """  
    with open(file_path, 'rb') as f:  
        return string_encoding(f.read())  
# 获取字符编码类型  
def string_encoding(b: bytes):  
    """ 
    获取字符编码类型\n 
    :param b: 字节数据\n 
    :return: \n 
    """  
    CODES = ['UTF-8', 'UTF-16', 'GB18030', 'BIG5']  
    # UTF-8 BOM前缀字节  
    UTF_8_BOM = b'\xef\xbb\xbf' 
    # 遍历编码类型  
    for code in CODES:  
        try:  
            b.decode(encoding=code)  
            if 'UTF-8' == code and b.startswith(UTF_8_BOM):  
                return 'UTF-8-SIG'  
            return code  
        except Exception:  
            continue  
    return '未知的字符编码类型'  
def readtxt(file_path):
    if file_encoding(file_path)=='GB18030':
        return open(file_path,'r').readlines()
    else:
        textlsit = []
        txte = open(file_path,'rb').readlines()
        for x in range(len(txte)):
            textlsit.append(txte[x].decode('utf-8'))#
        return textlsit

def readtxtline(file_path):
    if file_encoding(file_path)=='GB18030':
        text = ''
        tlist = open(file_path,'r').readlines()
        for i in tlist:
            text = text+i#+'\n'
        return text
    else:
        textlsit = []
        txte = open(file_path,'rb').readlines()
        for x in range(len(txte)):
            textlsit.append(txte[x].decode('utf-8'))#
        text = ''
        for i in textlsit:
            text = text+i#+'\n'
        return text
def readexcel(file_path):
    import xlrd
    book = xlrd.open_workbook(file_path)
    data = pandas.read_excel(file_path, sheetname=None)
    textdict = {};###用来构造{产品：{属性：text,属性:text}}这样的结构
    attrlist = ['肤感评论','气味评论','质地评论','效果评论','外观评论','价格评论','包装评论','评论']
    for sheet in book.sheets():
        for i in attrlist:
            
            #print(len(data[sheet.name][i]))
            cleans = data[sheet.name][i].dropna()#读取某列下的非空数值
            # print(type(data[sheet.name][i]))
            # print(addseries(cleans))
            textdict.setdefault(sheet.name, {})
            textdict[sheet.name].setdefault(i, addseries(cleans))
            
    print (textdict)
    return textdict
def addseries(series):
    text = ''
    for i in series:
        text = text+i+'\n'
    return text
#readexcel('沐浴露/整体数据1.xlsx')
if __name__ == '__main__':
    import xlrd
    book = xlrd.open_workbook('沐浴露/整体数据2.xlsx')
    attrlist = ['肤感评论','气味评论','质地评论','效果评论','外观评论','价格评论','包装评论','评论']
    for sheet in book.sheets():
        for i in attrlist:
            draw_wordcloud('沐浴露/整体数据2.xlsx','沐浴露',sheet.name,i)
    # print(file_encoding('敏感肌.txt'))
    # print(file_encoding('corpos.txt'))
    # print(readtxt('敏感肌.txt'))
    # print(readtxtline('corpos.txt'))
    # with open('corpos.txt') as f:
    #     content = f.read()
    # print(content)
    # print(type(content))
    # print(len(content))
    # print(content[13])
    # txte = open('敏感肌.txt','rb').readlines()#从文本中获取语料
    # #print(txte)
    # 

    # for x in range(len(txte)):
    #     textlsit.append(txte[x].decode('utf-8'))#
    # print(textlsit)

    # txte = open('corpos.txt','r').readlines()#从文本中获取语料
    # print(txte)