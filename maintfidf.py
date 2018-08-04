# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 17:55:17 2018

@author: user
"""
import MySQLdb
import re
import pandas as pd


def aksesstopword():
    stopword=[]
    con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='csv_db', charset='utf8')
    cur=con.cursor()
    cur.execute("SELECT kata from stopword")
    stpwrd=cur.fetchall()
    for stw in stpwrd:
        masuk=''.join(stw)
        stopword.append(masuk)
    con.commit()
    cur.close()
    return stopword

def artisingkat():   
    con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='csv_db', charset='utf8')
    cur=con.cursor()
    cur.execute("SELECT * from singkatan")
    singkatan=cur.fetchall()
    singkat=[sin[0] for sin in singkatan]
    arti={art[0]:art[1] for art in singkatan}
    con.commit()
    cur.close()
    return arti,singkat

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

def fulltfidf (dateList,semesta):
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
    remover=StopWordRemoverFactory()
    stoper=remover.create_stop_word_remover()
    factory=StemmerFactory()
    stemmer=factory.create_stemmer()
    tfidf=[]
    arti,singkat=artisingkat()
    stopword=aksesstopword()
    for v in dateList:
        naskah=[]
        for t in semesta:
            if t[1] == v:
                kecil=[]
                twit=[]
                twit=t[2].split(' ')
                for tw in twit:
                    tw=re.sub('[^A-Za-z ]+','',tw)
                    tw=tw.lower()
                    if tw in singkat:
                        tw=arti[tw]
                    kecil.append(tw)
                kec=' '.join(kecil)
                stemm=stoper.remove(kec)
                stemm=stemmer.stem(stemm)
                stop=stemm.split(' ')
                asli=[]
                for k in stop:
                    if k in stopword:
                        asli.append(k)
    
                naskah.append([t[0],t[1],' '.join(asli),asli,t[3],t[2]])
    
        wordset=set(naskah[0][3]).union(set(naskah[1][3]))
        for wor in naskah:
            if (wor[3]==naskah[0][3]) or (wor[3]==naskah[1][3]):
                pass
            else: wordset=set(wordset).union(set(wor[3]))
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
            stop_semen=[]
            for stops in stopword:
                if stops not in hasil_tfidf:
                    stop_semen.append(stops)
            hasil_tfidf.update(dict.fromkeys(stop_semen,0.0))
            datatfidf=pd.DataFrame.from_dict(hasil_tfidf)
            tfidf.append([tfbow[1][0],tfbow[1][1],tfbow[1][2],datatfidf,tfbow[1][4],tfbow[1][5]])
    
    return tfidf