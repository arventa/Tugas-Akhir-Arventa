# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 14:26:28 2018

@author: Arlan Arventa Gurusinga
for TF-IDF skripsweet 
"""

import re

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

def computeTFIDF(tfBow, idfs):
    tfidf={}
    for word, val in tfBow.items():
        tfidf[word]=[val*idfs[word]]
    return tfidf

import MySQLdb
#import datetime
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory=StemmerFactory()
stemmer=factory.create_stemmer()
#a= datetime.datetime.strptime("2018-01-10","%Y-%m-%d").date()
#dateList = []
#enddate=70
#for hari in range (0, enddate):
#    dateList.append(a + datetime.timedelta(days = hari))
stopword=[]
tfidf=[]
#Access DataBase
con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='csv_db', charset='utf8')
cur=con.cursor()
cur.execute("""SELECT * from dataset WHERE time_laps BETWEEN '2018-01-10' AND '2018-03-31';""")
banyak=cur.fetchall()
semesta=[]
dbtanggal=[]
for ban in banyak:
    semesta.append(list(ban))
    if ban[1] not in dbtanggal:
        dbtanggal.append(ban[1])
cur.execute("SELECT kata from stopword")
stpwrd=cur.fetchall()
listring=map(' '.join,stpwrd)
for stw in stpwrd:
    masuk=''.join(stw)
    stopword.append(masuk)
con.commit
cur.close()
#word=[]
#sentence=[]

#TFIDF Begin
tfidfs=[]
for v in dbtanggal:
    naskah=[]
    for t in semesta:
        if t[1]==v:    
            kecil=[]
            twit=[]
            twit=t[2].split(' ')
            for tw in twit:
                tw=re.sub('[^A-Za-z ]+','',tw)
                kecil.append(tw.lower())
            kec=' '.join(kecil)
            stemm=stemmer.stem(kec)
            stop=stemm.split(' ')
            asli=[]
            for k in stop:
                if k in stopword:
                    asli.append(k)
            
            naskah.append([t[0],t[1],stemm,stop,t[3]])

    wordset=set(naskah[0][3]).union(set(naskah[0][3]))
    for wor in naskah:
        wordset=set(wordset).union(set(wor[3]))
    wordDict=[]
    for a in naskah:
        wordDict.append(dict.fromkeys(wordset, 0))
    
    tfbows=[]
    for document in zip(naskah,wordDict):
        for word in document[0][3]:
            if word not in document[1]:
                document[1].update({word,0.0})
            else:
                document[1][word]+=1
        tfbows.append(computeTF(document[1],document[0][3]))
    idfs=computeIDF(wordDict)
    for tfbow in zip(tfbows,naskah):
        hasil_tfidf=computeTFIDF(tfbow[0],idfs)
        datatfidf=pd.DataFrame.from_dict(hasil_tfidf)
        tfidf.append([tfbow[1][0],tfbow[1][1],datatfidf,tfbow[1][4]])

datasvm=pd.DataFrame(tfidf)
##TFIDF End
#    
## SVM Begin
#import matplotlib.pyplot as plt
#from sklearn.model_selection import train_test_split
import pickle
#import numpy as np
svm_linear='svmlinear.sav'
svm_rbf='svmrbf.sav'
svm_poly='svmpoly.sav'
svm_sig='svmsigmoid.sav'
x=tfidf[0][2]
xindex=datasvm[0]
for fram in tfidf:
    if fram[0] == tfidf[0][0]:
        pass
    else:
        x=pd.concat([x,fram[2]], axis=0, ignore_index=True)
        x=x.fillna(0.0)
#    x=np.argwhere(np.isnan(x))
y=datasvm[3]
#X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.10) 
from sklearn.svm import SVC
clasifier_linear=SVC(kernel='linear')
clasifier_rbf=SVC(kernel='rbf')
clasifier_poly=SVC(kernel='poly')
clasifier_sig=SVC(kernel='sigmoid')

clasifier_linear.fit(x,y)
clasifier_rbf.fit(x,y)
clasifier_poly.fit(x,y)
clasifier_sig.fit(x,y)

#plt.scatter(xindex,y,color='black',label='data')
#plt.plot(xindex,clasifier_linear.predict(x),color='red',label='linear')
#plt.plot(xindex,clasifier_rbf.predict(x),color='green',label='rbf')
#plt.plot(xindex,clasifier_poly.predict(x),color='blue',label='polynomial')
#plt.plot(xindex,clasifier_sig.predict(x),color='yellow',label='sigmoid')

pickle.dumb(clasifier_linear, open(svm_linear,'wb'))
pickle.dumb(clasifier_rbf, open(svm_rbf,'wb'))
pickle.dumb(clasifier_poly, open(svm_poly,'wb'))
pickle.dumb(clasifier_sig, open(svm_sig,'wb'))



from sklearn.metric import classification_report, confusion_matix
y_pred=clasifier_linear.predict(x)
matrixy=confusion_matix(y,y_pred)
reporty=classification_report(y,y_pred)

#print('==============================')
#y_pred=clasifier_rbf.predict(X_test)
#print(confusion_matix(y_test,y_pred))
#print(classification_report(y_test,y_pred))
#print('==============================')
#y_pred=clasifier_poly.predict(X_test)
#print(confusion_matix(y_test,y_pred))
#print(classification_report(y_test,y_pred))
#print('==============================')
#y_pred=clasifier_sig.predict(X_test)
#print(confusion_matix(y_test,y_pred))
#print(classification_report(y_test,y_pred))
#print('==============================')
#print(y_pred,y_test)
#

