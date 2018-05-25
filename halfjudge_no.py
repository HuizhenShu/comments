# coding=utf-8
from test import sent2word
from emotionjudge import emotionjg
from emotionjudge import emotionjg_no
from txt2_list import txt2_list

import re
import nltk
def list2word(list):
  word = ''
  for i in list:
    word+=i
  #print(word)
  word = word.strip('\n').strip('\r\n').strip('\t').strip('\r').replace(',','').replace('，','').replace('\n','~').replace('\t','').replace('\r\n','').replace('\r','')
  #print(word)
  return word

#list2word(['你妹的,,,\n','呵呵哒'])
####添加其他词库，出现其他词的半句删除
# pposwords = []
# pposwords = txt2_list(r'沐浴露词库\沐浴露词库\专业\沐浴露正面.txt',pposwords)
# pnegwords = []
# pnegwords = txt2_list(r'沐浴露词库\沐浴露词库\专业\沐浴露负面.txt',pnegwords)

# poswords = []
# poswords = txt2_list(r'沐浴露词库\沐浴露词库\通用\正面情绪.txt',poswords)
# negwords = []
# negwords = txt2_list(r'沐浴露词库\沐浴露词库\通用\负面情绪.txt',negwords)
# tywords = []
# tywords = txt2_list(r'沐浴露词库\沐浴露词库\通用\通用词语.txt',tywords)
# alllist = [smelllist,zhidilist,skinlist,effectlist,looklist,packagelist,pricelist,otherlist,poswords,negwords,pposwords,pnegwords,tywords]
# allcontent = ['气味','质地','肤感','效果','外观','包装','价格','删除半句库','正面','负面','沐浴露正面','沐浴露负面','通用词库']
ff = '一直都是用相宜本草，我也只能用这个牌子才不过敏，卸妆很好，用其他的都会过敏，之前都是在实体店购买，随便买个水水和霜霜什么的就要几百块钱了，虽然也有很多赠品。这次双十一买了超级多，囤了一大堆的货，估计可以用到明年的双十一了，很开心有双十一的这些优惠活动，也很期待下一次优惠活动哦。虽然遇到了一点点小插曲，后来都愉快的解决了'
#print (sent2word(ff))
def splitsent(sent,files):

    spsent = re.split('[，。,.；;!?！？ ...~~、…]',sent)
    skinw =0
    zhidiw = 0
    effectw = 0
    smellw = 0
    lookw = 0
    packagew = 0
    pricew = 0

    skins =[]
    zhidis = []
    effects = []
    smells = []
    looks = []
    packages = []
    prices = []

    lenskinw =0
    lenzhidiw = 0
    leneffectw = 0
    lensmellw = 0
    lenlookw = 0
    lenpackagew = 0
    lenpricew = 0
    print(spsent)
    for i in spsent:
       #print (sent2word(i))
       for q in otherlist:
         if q in i:
          if i in spsent:
              spsent.remove(i)
              #print(i)
    print(spsent)
    for i in spsent:
       #print (sent2word(i))
       for j in smelllist:
         if j in i:
          smells.append(i)
          lensmellw+=1
          smellw=smellw+emotionjg_no(i,files)
          print (i)
       for j in skinlist:
         if j in i and '干净' not in i and '细腻' not in i:
          skins.append(i)
          lenskinw+=1
          skinw=skinw+emotionjg_no(i,files)
          print (i)
       for j in zhidilist:
         if j in i and '稀巴烂' not in i:
          zhidis.append(i)
          lenzhidiw+=1
          zhidiw=zhidiw+emotionjg_no(i,files)
          print (i)
       for j in effectlist:
         if j in i:
          effects.append(i)
          leneffectw+=1
          effectw=effectw+emotionjg_no(i,files,2)
          print (i)
       for j in looklist:
         if j in i and '完美' not in i and '依旧' not in i:
          looks.append(i)
          lenlookw+=1
          lookw=lookw+emotionjg_no(i,files)
          print (i)
       for j in packagelist:
         if j in i:
          packages.append(i)
          lenpackagew+=1
          packagew=packagew+emotionjg_no(i,files)
          print (i)
       for j in pricelist:
         if j in i:
          prices.append(i)
          lenpricew+=1
          pricew=pricew+emotionjg_no(i,files)
          print (i)
    # print(sent)
    # print('total:'+str(emotionjg(sent)))
    # print(smellw)
    # print('smell:'+str(emotionjg(smellw)))
    # print(skinw)
    # print('skin:'+str(emotionjg(skinw)))
    # print(zhidiw)
    # print('zhidi:'+str(emotionjg(zhidiw)))
    # print(effectw)
    # print('effect:'+str(emotionjg(effectw)))
    # print(lookw)
    # print('look:'+str(emotionjg(lookw)))
    smells = list2word(list(set(smells)))
    skins = list2word(list(set(skins)))
    zhidis = list2word(list(set(zhidis)))
    effects = list2word(list(set(effects)))
    looks = list2word(list(set(looks)))
    packages = list2word(list(set(packages)))
    prices = list2word(list(set(prices)))
    totalw= 0
    for i in spsent:
       totalw+=emotionjg_no(i,files)
    print('total:',totalw,'skin:',skinw,'smell:',smellw,'zhidi:',zhidiw,'effect:',effectw,'look:',lookw,'price:',pricew,'肤感:',skins,'气味:',smells,'质地:',zhidis,'效果:',effects,'外观:',looks,'价格:',prices,'包装:',packages) 
    return totalw,1,skinw,lenskinw,smellw,lensmellw,zhidiw,lenzhidiw,effectw,leneffectw,lookw,lenlookw,pricew,lenpricew,packagew,lenpackagew,skins,smells,zhidis,effects,looks,prices,packages
if __name__ == '__main__':
  prolist = ['舒适达牙膏.csv']#','多芬衡悦水润沐浴乳.csv','力士爽肤闪亮冰爽沐浴露.csv','六神冰凉超爽沐浴乳.csv','舒肤佳柠檬清新沐浴露.csv','资生堂可悠然美肌沐浴露 500ml（欣怡幽香恬静清香）.csv','蜕唤美小黑裙沐浴露.csv','COCOVEL香体沐浴露.csv','KJU木槿花香济之州宠肤沐浴露套装.csv','东方宝石水润嫩肤香氛沐浴露(水莲花香）500ml.csv','蔻斯汀樱花花瓣沐浴露沐浴液500ml.csv','力士精油香氛沐浴露幽莲魅肤1KG.csv'
  ##'欧莱雅火山岩洗面奶洁面乳.csv','妮维雅洗面奶洁面乳.csv','佰草世家洗面奶洁面乳.csv','瓷肌洗面奶洁面乳.csv','修正洗面奶洁面乳.csv','凌仕洁容膏.csv'
  resultlist =  ['舒适达牙膏1.csv']#'力士精油香氛沐浴露幽莲魅肤1KG1.csv'
  #[]#'欧莱雅.csv','妮维雅.csv','佰草世家.csv','瓷肌.csv','修正.csv','凌仕.csv'
  mebrandlist = ['舒适达']#'滴露','多芬','力士','六神','舒肤佳','资生堂','蜕唤美','蔻露薇','KJU','东方宝石','蔻斯汀',
  sqelist = ['牙膏']
  #splitsent('不好','牙膏')
  for p in sqelist:
    smelllist=[]
    smelllist = txt2_list(r'%s\专业\属性\气味.txt'%p,smelllist)

    zhidilist = []
    zhidilist = txt2_list(r'%s\专业\属性\质地.txt'%p,zhidilist)

    skinlist = []
    skinlist = txt2_list(r'%s\专业\属性\肤感.txt'%p,skinlist)

    effectlist = []
    effectlist = txt2_list(r'%s\专业\属性\效果.txt'%p,effectlist)

    looklist = []
    looklist = txt2_list(r'%s\专业\属性\外观.txt'%p,looklist)

    packagelist = []
    packagelist = txt2_list(r'%s\通用\属性\包装.txt'%p,packagelist)

    pricelist = []
    pricelist = txt2_list(r'%s\通用\属性\价格.txt'%p,pricelist)

    otherlist = ['其他','另外','以前','肤质偏油','肤质偏干','某牌','某大牌','原来','专柜','说明书','别的','实体店','敏感肌','敏感肌肤','敏感皮肤','过敏皮肤','之前','那款','旧版','旧款','老款','店里的',
    '店里','旧包装','油皮','干皮','混油','干性肤质','别人','其它','去年','期待','希望','期望','专卖店','敏感性皮肤','现实店铺','商场','中性偏干性皮肤','油性','中性皮肤','干燥皮肤',
    '家乐福','沃尔玛','华联','联华','乐购','大润发','之前','人家','试用装','应该','原以为','那种','屈臣氏','别的','花粉过敏','新款','评论','评价','本来','以为',
    '如果','赠品','估计','商场','考虑','邮费','运费','淘金币','那款','银泰','掌柜','卖家','微博','客服','舍友','知乎','天猫超市','好多人','同类','说的','应该','责任心','老板',
    '店家','超市','亚马逊','聚美','店铺','屈臣氏','态度','服务','收件']
    otherlist = txt2_list(r'%s\品牌词库.txt'%p,otherlist)
    otherlist = txt2_list(r'%s\品类词库.txt'%p,otherlist)
    for j in range(len(prolist)):
      comment = open(r'%s\%s' % (p,prolist[j]),'r',encoding='utf-8',errors='ignore')#韩束墨菊洗面奶洁面乳、百雀羚洗面奶水能量焕采洁容膏、自然堂雪润深澈洁面膏、Olay玉兰油氨基酸洗面奶女新生焕活深彻洁面乳\相宜本草山茶花焕活净颜乳
      commentw = open(r'%s\%s' % (p,resultlist[j]),'w',encoding='utf-8',errors='ignore')#百雀羚
      commentw.write('总体'+','+'总体长度'+','+'肤感'+','+'肤感长度'+','+'气味'+','+'气味长度'+','+'质地'+','+'质地长度'+','+'效果'+','+'效果长度'+','+'外观'+','+'外观长度'+','+'价格'+','+'价格长度'+','+'包装'+','+'包装长度'+','+'肤感评论'+','+'气味评论'+','+'质地评论'+','+'效果评论'+','+'外观评论'+','+'价格评论'+','+'包装评论'+','+'评论'+'\n')#

      commentline = comment.readlines()
      commenttext = ''
      #mebrand = ['牙膏'] #'韩束'''相宜本草','相宜''玉兰油','兰油''自然堂''百雀羚','百雀''芙丽芳丝' 
      # brand = open(r'词库\护肤.txt','r',encoding='utf-8',errors='ignore')
      
      #otherlist = txt2_list(r'牙膏\品类词库.txt',otherlist)
      # for i in mebrand:
      #     if i in otherlist:
      #        print(i)
      #print(otherlist)
      #print(mebrand)
      if p in otherlist:
        print('yes')
        otherlist.remove(p)
      otherlist.remove(mebrandlist[j])
      for i in commentline:
          i = i.replace('\ue600','').replace('\ue601','')
          score = splitsent(i,p)
          # print(score)
          # print(len(score))
          commentw.write('')
          for j in score:
              #print(str(j)+'hehe')
              commentw.write(str(j)+',')  
          commentw.write(i)
      commentw.close()    
      comment.close()
        


# unicharset_extractor merge.2.box merge.3.box merge.4.box merge.5.box merge.6.box merge.7.box merge.8.box merge.9.box merge.10.box 
# mftraining -F font -U unicharset merge.2.tr merge.3.tr merge.4.tr merge.5.tr merge.6.tr merge.7.tr merge.8.tr merge.9.tr merge.10.tr 
# why.3.tr why.4.tr why.5.tr why.3.tr why.4.tr why.5.tr why.3.tr why.4.tr why.5.tr

##跑出分词结果是否在词库中  
    # commentline = comment.readlines()
    # commenttext = ''
    # def float(n):
    #         try:
    #             n.strip("\n").strip("\t")
    #             return False
    #         except:
    #             return True
    # for i in commentline:
    #         ftt = i.strip("\n").strip("\t")#.replace('\ufeff','').replace('\ue600','').replace('\ue601','').replace('\xeb','').replace('\xfb','').replace('\u20ac','')
    #         #print(sent2word(ftt))
    #         #fenciresult.write(sent2word(ftt))
    #         commenttext = commenttext+ftt
    # text = sent2word(commenttext)
    # #print(text)
    # word_lst = text.split(' ')#list
    # wordfre = nltk.FreqDist(word_lst)
    # textfre = open(r'词频%s'%prolist[j],'w',encoding='utf-8',errors='ignore')
    # #print(wordfre.most_common(1000))
    # # # print(len(wordfre.most_common()))
    
    
    # for i in wordfre.most_common(len(wordfre.most_common())):
    #     tag = ''
    #     for q in range(len(alllist)):
    #         if str(i[0]) in alllist[q]:
    #             tag=tag+','+allcontent[q]
    #     textfre.write(str(i[0])+','+str(i[1])+','+tag+'\n')
      ##跑出分词结果是否在词库中
