# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 15:53:47 2018

@author: user
"""
def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

def computeIDF(docList):
    import math
    idfDict = {}
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))
        
    return idfDict

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return tfidf
import datetime
docA = ["Indonesia berhasil menjadi pemilik saham mayoritas",datetime.datetime.strptime("10-02-2018","%d-%m-%Y"),"positive",'1']
docB = ["Freeport adalah perusahaan tambang terbesar di Indonesia",datetime.datetime.strptime("10-02-2018","%d-%m-%Y"),"negative",'2']
docC = ["Setelah 50 tahun Indonesia hanya mendapat bagian kecil",datetime.datetime.strptime("10-02-2018","%d-%m-%Y"),"positive",'3']
docD = ["Bahkan rakyat papua tidak dapat menikmati hasil tanahnya sendiri",datetime.datetime.strptime("11-02-2018","%d-%m-%Y"),"negative",'4']
docE = ["Ini adalah sebuah langkah yang berani",datetime.datetime.strptime("11-02-2018","%d-%m-%Y"),"positive",'5']
docF = ["Belum ketahuan apakah langkah yang baik atau buruk",datetime.datetime.strptime("11-02-2018","%d-%m-%Y"),"negative",'6']
docG = ["Yang jelas ini akan menjadi sebuah batu loncatan untuk pertambangan Indonesia",datetime.datetime.strptime("12-02-2018","%d-%m-%Y"),"positive",'7']
docH = ["Disaat tambang terbesar didunia dikelola oleh anak-anak muda Indonesia",datetime.datetime.strptime("12-02-2018","%d-%m-%Y"),"negative",'8']
docI = ["Menjadi tuan di rumah sendiri.",datetime.datetime.strptime("12-02-2018","%d-%m-%Y"),"positive",'9']
documents=[]
documents.append(docA)
documents.append(docB)
documents.append(docC)
documents.append(docD)
documents.append(docE)
documents.append(docF)
documents.append(docG)
documents.append(docH)
documents.append(docI)
a = datetime.datetime.strptime("10-02-2018","%d-%m-%Y")
numdays = 3
dateList = []
for x in range (0, numdays):
    dateList.append(a + datetime.timedelta(days = x))
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory=StemmerFactory()
stemmer=factory.create_stemmer()
stopword=['hasil','jadi','anak','langkah','dapat','milik','freeport','tambang','saham','indonesia']
tfidfs=[]
xgede=[]
ygede=[]
#doku=[]
for v in dateList:
#    print('ok')
    doku=[]
    for t in documents:
        
        if t[1]==v:
            asli=[]
            yak=t[0].split(' ')
            kecil=[]
            for kata in yak:
                kecil.append(kata.lower())
            kec=' '.join(kecil)
            stemming=stemmer.stem(kec)
            stemm=stemming.split(' ')
            for k in stemm:
                if k in stopword:
                    asli.append(k)
#            docs=[]
            docs=' '.join(asli)
            doku.append([docs,asli,t[1],t[2]])
#    if len(semen)>0:
#        doku.append(semen)

    bows=[]
    for per in doku :
        bows.append(per[1])
    wordset=set(bows[0]).union(set(bows[1]))
    for wob in bows:
        wordset=set(wordset).union(set(wob))
    wordDict=[]
    for a in bows:
        wordDict.append(dict.fromkeys(wordset, 0))
    tfbows=[]
    for document in zip(doku,bows,wordDict):
        for k in document[0][1]:
            if k not in stopword:
                document[2].update({k,0.0})
            else:
                document[2][k]+=1
                    
        tfbows.append(computeTF(document[2],document[1]))
    idfs=computeIDF(wordDict)
    tfidftemp=[]
    for tfbow in zip(tfbows,doku):
        tfidftemp.append([computeTFIDF(tfbow[0],idfs),tfbow[1][1],tfbow[1][2],tfbow[1][3]])
#        semen=[]
#        for stop in stopword:
#            for d in doku:
#                if stop not in d:
#                    semen.append(stop)
#        tfidftemp.append(dict.fromkeys(semen,0.0))
    tfidfs.append(tfidftemp)


    

#from sklearn.svm import SVC
#import numpy as np
#predik=SVC(kernel='rbf')
#xgede=np.array(xgede)
#ygede=np.array(ygede)
#predik.fit(xgede,ygede)