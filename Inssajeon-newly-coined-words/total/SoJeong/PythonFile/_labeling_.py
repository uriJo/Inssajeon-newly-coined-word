# -*- coding: utf-8 -*-
from konlpy.tag import Kkma
from konlpy.tag import Komoran
import pandas as pd
import re

komoran = Komoran()
kkma = Kkma()

fileFor = pd.read_csv('/Text/Category/forSojung.csv', header=1, names = ["word"])
file = open('/Text/Category/label.txt')

fileList = []
for i in file:
    i =re.sub('\n', '',i)
    fileList.append(i)

ff = list(fileFor["word"])
ff = list(set(ff))
fileList.extend(ff)


catecory = open('/Result/category.txt','w',encoding='utf-8')
pp = open('/Result/pos.txt','w',encoding='utf-8')
means = open('/Result/emiMeans.txt')

meansDic = {}
for i in means:
    s = i.split('-')
    meansDic[s[0]] = s[1]

emi1 = []
emi2 = []
emi3 = []

EMI1 = ['병','남','족','러','력','템','체']
EMI2 = ['캉스','세권','세대','알못','잘알','주의','빌런','그램','만랩','린이','문화','그로','만추','푸어']
EMI3 = ['리단길', '포비아','플레인','증후군','플렉스','니스트','팡질팡','파라치','노믹스']
PRE1 = ['핵']
PRE2 = ['갑분']
PRE3 = []

for i in fileList:
    if len(i) > 6:
        fileList.remove(i)
        emi.append(i)

for i in EMI1:
    for j in fileList:
        if len(j) > 1:
            if i == j[len(j)-1]:
                fileList.remove(j)
                emi1.append(j)

for i in EMI2:
    for j in fileList:
        if len(j) > 2:
            if i == j[len(j)-2:]:
                fileList.remove(j)
                emi2.append(j)

for i in EMI3:
    for j in fileList:
        if len(j) > 3:
            if i == j[len(j)-3:]:
                fileList.remove(j)
                emi3.append(j)

ko = []
for i in fileList:
    ko.append(i)

noun = []
other = []

#헤더
catecory.write('word' + ' ' + "label(ko)" +' ' + "label(num)"+ '\n')
pp.write("pos"+ '\n')

#예외사항 : '혼-'
for i in ko:
    if i[0][0] =='혼' and len(i) ==2:
        ko.remove(i)
        po = komoran.pos(i)
        for j in po:
            pp.write(j[1]+" ")
        pp.write('\n')
        catecory.write(i+ ' 줄임말' + " "+"1" +'\n')


for i in ko:
    if len(i) == 3 and len(i) == len(komoran.pos(i)):
        ff += 1
        ko.remove(i)
        po = komoran.pos(i)
        for j in po:
            pp.write(j[1] + " ")
        pp.write('\n')
        catecory.write(i + ' 줄임말' + " " + "1" + '\n')
    else:
        pass

for i in ko:
    kk = komoran.pos(i)
    for k in kk:
        if k[1] == ('NNG') or k[1] == ('NNP') or k[1] == ('NNB') or k[1] == ('NP') or k[1] == ('NR'):
            noun.append(i)
            break
        else:
            other.append(i)
            break
            
# 'NA'(형태소 파악 불가 태깅) 저장
remove= []

for i in other:
    count +=1
    pos = komoran.pos(i)
    if pos[0][1] ==('NNG') or pos[0][1] ==('NNP') or pos[0][1] ==('NNB') or pos[0][1] ==('NP') or pos[0][1] ==('NR'):
        for j in pos:
            pp.write(j[1]+" ")
        pp.write('\n')
        catecory.write(i + ' 줄임말' + ' ' + "1" + '\n')
    elif pos[0][1] ==('NA'):
        remove.append(i)
        other.remove(i)
    else:
        for j in pos:
            pp.write(j[1]+" ")
        pp.write('\n')
        catecory.write(i+ ' 미정' + ' '+ "2" + '\n')

for i in noun:
    count += 1
    pos = komoran.pos(i)
    for j in pos:
        pp.write(j[1] + " ")
    pp.write('\n')
    catecory.write(i + ' 합성어' + ' '+ "0" + '\n')

for i in remove:
    count += 1
    kopos = kkma.pos(i)
    if len(i) <=2:
        for j in kopos:
            pp.write(j[1] + " ")
        pp.write('\n')
        catecory.write(i +' 줄임말' + " 1" + '\n')
    elif len(i) <= len(kopos):
        for j in kopos:
            pp.write(j[1] + " ")
        pp.write('\n')
        catecory.write(i + ' ' + '줄임말' + " 1" + '\n')
    else:
        for j in kopos:
            pp.write(j[1] + " ")
        pp.write('\n')
        catecory.write(i + ' ' + '합성어' + " 0" + '\n')

catecory.close()
pp.close()

catecoryPD = pd.read_csv('/Result/category.txt', sep = ' ')
#catecory  = catecory.sample(frac=1).reset_index(drop=True)
catecoryPD.to_csv('/Result/category.csv', encoding='utf-8')
catecoryPD.to_csv('/Result/categorySelf.csv', encoding='utf-8')

