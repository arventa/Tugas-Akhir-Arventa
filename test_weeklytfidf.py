# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 12:44:35 2018

@author: user
"""

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
import datetime
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory=StemmerFactory()
stemmer=factory.create_stemmer()

#Access DataBase
con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='csv_db', charset='utf8')
cur=con.cursor()
cur.execute("""SELECT * from dataset WHERE time_laps BETWEEN '2018-01-10' AND '2018-03-31';""")
banyak=cur.fetchall()
semesta=[]
stopword=[]
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
#Close DataBase

a= datetime.datetime.strptime("2018-01-07","%Y-%m-%d").date()
dateList = []
enddate=100
for hari in range (0, enddate):
    weeklist=[]
    for perday in range(0,7):
        weeklist.append(a + datetime.timedelta(days = perday))
    a=(weeklist[-1] + datetime.timedelta(days=1))
    dateList.append(weeklist)
    if a not in dbtanggal:
        break
#TFIDF Begin
tfidf=[]
for v in dbtanggal:
    naskah=[]
    for t in semesta:
        if t[1]in v:    
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
            document[1][word]+=1
        tfbows.append(computeTF(document[1],document[0][3]))
    idfs=computeIDF(wordDict)
    for tfbow in zip(tfbows,naskah):
        hasil_tfidf=computeTFIDF(tfbow[0],idfs)
        datatfidf=pd.DataFrame.from_dict(hasil_tfidf)
        tfidf.append([tfbow[1][0],tfbow[1][1],datatfidf,tfbow[1][4]])
#
datasvm=pd.DataFrame(tfidf)
##TFIDF End
#    
## SVM Begin
#import matplotlib.pyplot as plt
#from sklearn.model_selection import train_test_split
import pickle
#import numpy as np
svm_linear='svmlinearweekly.sav'
svm_rbf='svmrbfweekly.sav'
svm_poly='svmpolyweekly.sav'
svm_sig='svmsigmoidweekly.sav'
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

## Start Train SVC
#from sklearn.svm import SVC
#clasifier_linear=SVC(kernel='linear')
#clasifier_rbf=SVC(kernel='rbf')
#clasifier_poly=SVC(kernel='poly')
#clasifier_sig=SVC(kernel='sigmoid')
#
#clasifier_linear.fit(x,y)
#clasifier_rbf.fit(x,y)
#clasifier_poly.fit(x,y)
#clasifier_sig.fit(x,y)

#plt.scatter(xindex,y,color='black',label='data')
#plt.plot(xindex,clasifier_linear.predict(x),color='red',label='linear')
#plt.plot(xindex,clasifier_rbf.predict(x),color='green',label='rbf')
#plt.plot(xindex,clasifier_poly.predict(x),color='blue',label='polynomial')
#plt.plot(xindex,clasifier_sig.predict(x),color='yellow',label='sigmoid')

#pickle.dumb(clasifier_linear, open(svm_linear,'wb'))
#pickle.dumb(clasifier_rbf, open(svm_rbf,'wb'))
#pickle.dumb(clasifier_poly, open(svm_poly,'wb'))
#pickle.dumb(clasifier_sig, open(svm_sig,'wb'))
#End of Train SVC

#Start Test SVC
testsvm_linear = pickle.load(open(svm_linear, 'rb'))
testsvm_poly = pickle.load(open(svm_poly, 'rb'))
testsvm_rbf = pickle.load(open(svm_rbf, 'rb'))
testsvm_sig = pickle.load(open(svm_sig, 'rb'))

#report classification
from sklearn.metric import classification_report
y_linear=testsvm_linear.predict(x)
#matrixy_lin=confusion_matix(y,y_linear)
reporty_lin=classification_report(y,y_linear)

y_poly=testsvm_poly.predict(x)
#matrixy_poly=confusion_matix(y,y_poly)
reporty_poly=classification_report(y,y_poly)

y_rbf=testsvm_rbf.predict(x)
#matrixy_rbf=confusion_matix(y,y_rbf)
reporty_rbf=classification_report(y,y_rbf)

y_sig=testsvm_sig.predict(x)
#matrixy_sig=confusion_matix(y,y_sig)
reporty_sig=classification_report(y,y_sig)
#
##save data to db
#con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='csv_db', charset='utf8')
#cur=con.cursor()
#cur.execute("""CREATE TABLE IF NOT EXISTS after_svm (id_str varchar(18), tanggal date, class_manual varchar(8), class_linear varchar(8), class_poly varchar(8), class_rbf varchar(8), class_sig varchar(8), PRIMARY KEY(id_str))""")
#eksekution="""INSERT INTO after_svm VALUES (%s %s %s %s %s %s %s)"""
#to_db=[(x[0][0], x[0][1], x[0][3], x[1], x[2], x[3])for x in zip(tfidf,y_linear,y_poly,y_rbf,y_sig)]
#cur.executemany(eksekution,to_db)
#con.commit()
#con.close()

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

