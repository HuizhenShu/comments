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
def txt2_list(data,listwords):
    #txt = open(data,'r',encoding='utf-8',errors='ignore')

    txtlines = readtxt(data)

    for i in range(1,len(txtlines)):
        listword = txtlines[i].strip("\n").strip("\r")
        listwords.append(listword)
    #print(listwords)
    return listwords
# def list2_txt(list):
#     txt = open(data,'w',encoding='utf-8',errors='ignore')

#     listwords = []
#     txtlines = txt.readlines()
#     for i in range(0,len(txtlines)):
#         listword = txtlines[i].strip("\n")
#         listwords.append(listword)
#     print(listwords)
#     return listwords
if __name__ == '__main__':
	listwords=[]
	txt2_list(r'词库\正面(4).txt',listwords)