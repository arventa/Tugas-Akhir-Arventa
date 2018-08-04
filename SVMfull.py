# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 18:11:56 2018

@author: user
"""
import pandas as pd
import pickle
from sklearn.svm import SVC,SVR
import numpy as np
    
def SVCxy(tfidf,datasvm):
    x=tfidf[0][3]
    for fram in tfidf:
        if fram[0] == tfidf[0][0]:
            pass
        else:
            x=pd.concat([x,fram[3]], axis=0, ignore_index=True)
    y=datasvm[4]
    return x,y

def SVCtrain(x,y,svm_linear):
    clasifier_linear=SVC(kernel='linear')
    clasifier_linear.fit(x,y)
    pickle.dump(clasifier_linear, open(svm_linear,'wb'))
    
def SVCtest(x,y,svm_linear):
    from sklearn.metrics import classification_report
    testsvm_linear = pickle.load(open(svm_linear, 'rb'))
    y_linear=testsvm_linear.predict(x)
    reporty_lin=classification_report(y,y_linear)
    print('linear : ',reporty_lin)
    framey_lin=list(y_linear)
    return framey_lin


def rmse(predictions, targets):
    return np.sqrt(((np.array(predictions) - np.array(targets)) ** 2).mean())

def xypredic(indexx,dateList,data):
    dset=[]
    xplot=[]
    for tanggal in dateList:
        y_positive=0
        y_negative=0
        for d in data:
            if d[1] in tanggal:
                if d[3]=='positive':
                    y_positive+=1
                elif d[3]=='negative':
                    y_negative+=1
        
        if y_positive>0:
            indexx+=1
            xplot.append(indexx)
            dset.append([indexx,y_positive,y_negative])
    
    #import numpy as np
    xy=pd.DataFrame(dset)
    x=xy.iloc[:,:-1]
    y_pos=xy.iloc[:,1]
    y_neg=xy.iloc[:,2]
    
    return x,y_pos,y_neg,xplot

def SVRtrain(x,y,filename):
    svr=SVR(kernel='linear')
    svr.fit(x,y)
    pickle.dump(svr,open(filename,'wb'))
    
def SVRtest(x,y,filename):
    test=pickle.load(open(filename,'rb'))
    predict=test.predict(x)
    akurasi=rmse(predict,y)
    return predict,akurasi
