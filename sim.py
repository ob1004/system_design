# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 17:58:07 2021

@author: Administrator
"""
import csv
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack
import numpy as np
import scipy
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

import jieba
import time
                
corpus=[]  
alltime=[]    
annid=[]         
with open('Control_Date.csv','r') as file:
    file.readline()
    reader=csv.reader(file)
    
    for line in reader:
        cutc=(jieba.cut(line[5],cut_all=False))
        temp=[]
        for i in cutc:
            temp.append(i)
        res=' '.join(temp)
        corpus.append(res)
        timeStruct = time.strptime(line[3], "%Y-%m-%d") 
        ts = int(time.mktime(timeStruct))         
        alltime.append(ts)
        annid.append(line[4])
        
control=len(corpus)
      
treat=[]  
with open('Treat_Date.csv','r') as file:
    file.readline()
    reader=csv.reader(file)
    for line in reader:
        cutc=(jieba.cut(line[5],cut_all=False))
        temp=[]
        for i in cutc:
            temp.append(i)
        res=' '.join(temp)
        corpus.append(res)
        treat.append(res)
        timeStruct = time.strptime(line[3], "%Y-%m-%d") 
        ts = int(time.mktime(timeStruct))         
        alltime.append(ts)
        annid.append(line[4])

        
centroids = []
vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
vfit=vectorizer.fit_transform(corpus)
tfidf=transformer.fit_transform(vfit)#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵

for i in range(len(corpus)):
    if i%100==0:
        print(i)
    test_count=vectorizer.transform([corpus[i]])
    test_tfidf = transformer.transform(test_count)
    a=sparse.csr_matrix(test_tfidf.toarray())
    c = a.astype('float16')
    centroids.append(c)


c = vstack(centroids, format="csr")
similarities = cosine_similarity(c)


result=[]
for i in range(control,len(corpus)):
    smaxm=similarities[i,0:control]
    smax=max(smaxm)
    temp=[]
    for j,k in enumerate(smaxm):
        if k==smax:
            temp.append(j)
    if len(temp)>1:
        thr=9000000000
        zzz=0
        for a in temp:
            print(corpus[a])
            print(alltime[a])
            diff=abs(alltime[a]-alltime[i])
            if diff<=thr:
                thr=diff
                zzz=a
        result.append((annid[i],annid[zzz]))
        print(zzz)
    else:
        result.append((annid[i],annid[temp[0]]))
        
out1 = open('ressss.csv','w', newline='',encoding='utf-8-sig')
csv_write=csv.writer(out1,dialect='excel')    

for i in result:
    csv_write.writerow([i[0],i[1]])
out1.close()