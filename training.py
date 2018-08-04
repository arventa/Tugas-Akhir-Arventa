# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 14:26:28 2018

@author: Arlan Arventa Gurusinga
for TF-IDF skripsweet 
"""
import re
import pandas as pd
#from sklearn.linear_model import LogisticRegression
#import numpy as np
#from sklearn.feature_extraction.text import TfidfVectorizer

def computeTF(wordDict, bow):
    tfDict={}
    bowCount=len(bow)
    for word,count in wordDict.items():
        tfDict[word]=count/float(bowCount)
    return tfDict

def computeIDF(docList):
    import math
    idfDict={}
    N=len(docList)
    idfDict=dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val>0:
                idfDict[word]+=1
    for word, val in idfDict.items():
        idfDict[word]=math.log10(N/float(val))
    return idfDict

def computetfidf(tfBow, idfs):
    tfidf={}
    for word, val in tfBow.items():
        tfidf[word]=val*idfs[word]
    return tfidf

#model_tfidf='trainidf.sav'
#wordA = 'Menyusul masuknya Netflix di Indonesia pada bulan Januari 2016, Grup Telkom, termasuk IndiHOME memblokir layanan tersebut. Beberapa pengguna yang ingin mengakses Netflix kemudian memindahkan penyedia layanan pada perusahaan lain, dan mendapati bahwa nomor telepon rumahnya yang telah digunakan selama puluhan tahun ikut dicabut. Namun sebagai Jawaban atas kontroversi ini, kini IndiHome menyediakan layanan DUAL PLAY dan TRIPLE PLAY.'
#wordB = '"Berhenti Langganan IndiHome, Telepon Rumah Juga Dicabut?". kompas.com. Diakses tanggal 2 Februari 2016. Layanan Indihome Telkom kini seolah menjadi bumerang bagi pengguna yang ingin berhenti berlangganan. Pasalnya, jika ingin berhenti layanan internetnya, maka semua produk Telkom yang ada akan dicabut, termasuk telepon rumah.'

import MySQLdb
con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='csv_db', charset='utf8')
cur=con.cursor()
cur.execute("SELECT text from dataset")
word=[]
words=[]
bowx=[]
for rowkata in cur:
#    bowx.append(x.split(' '))
#    wordset=set(x.split(' ')).union(set(word))
    x=' '.join(rowkata)
    re.sub('[^A-Za-z0-9 ]+', '', x)
    x.lower()
    word.append(x)
stopword=[]
cur.execute("select kata from corpus")
for i in cur:
    stopword.append(i)
#for k in words:
#    str(k)
#    k = re.sub('[^A-Za-z0-9 ]+', '', k)
#    k = k.lower()
#    word.append(k)

#wordB = re.sub('[^A-Za-z0-9 ]+', '', wordB)
#wordB = s.lower() for s in wordB//
#wordB = wordB.lower()

#bowA=wordA.split(' ')
#bowB=wordB.split(' ')

bow=word.split(' ')

#wordSet=set(bowA).union(set(bowB))
wordset=set(bow)
#wordDictA=dict.fromkeys(wordSet,0)
#wordDictB=dict.fromkeys(wordSet,0)
wordDict=dict.fromkeys(wordset,0)


for bow in bowx:
    wordDict[bow]+=1

#for word in bowB:
#    wordDictB[word]+=1

pd.DataFrame(wordDict)
tfbow=computeTF(wordDict, bowx)
#tfbowB=computeTF(wordDictB, bowA)
idfs=computeIDF(wordDict)

tfidfbow=computetfidf(tfbow, idfs)
#tfidfbowB=computetfidf(tfbowB, idfs)
pd.DataFrame(tfidfbow)

#import MySQLdb
#con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='csv_db', charset='utf8')
#cur=con.cursor()
#cur.execute("CREATE TABLE bobot (id_str varchar(18),time_laps date,text varchar(153),sentiment varchar(8), PRIMARY KEY(id_str));")
#
#
#cur.executemany("INSERT INTO dataset VALUES (%s, %s, %s, %s);", to_db)
#con.commit()

#picklesetX=[]
#picklesetY=[]
#model=LogisticRegression()
#model.fit(tfidfbowA,tfidfbowB)
#picklesetX = np.array(picklesetX)
#picklesetY = np.array(picklesetY)
#tfidfbowA.fit(picklesetX,picklesetY)
#pickle.dump(model, open(model_tfidf,'wb'))
#computetfidf.fit([tfbowA, tfbowB], idfs)
#tfidf=TfidfVectorizer()
#response = tfidf.fit_transform([wordA,wordB])
#feature_names = tfidf.get_feature_names()
#for col in response.nonzero()[1]:
#    print(feature_names[col], '-', response[0,col])
#pickle.dump(model_tfidf, open([tfidfbowA, tfidfbowB],'wb'))