# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 13:40:56 2018

@author: user
"""
import SVMfull as svm
import MySQLdb
import datetime

#gojek hhrhrhrhaaaaaa

a= datetime.datetime.strptime("2018-04-30","%Y-%m-%d").date()
con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='100an', charset='utf8')
cur=con.cursor()
cur.execute("SELECT * FROM dataset WHERE time_laps BETWEEN '2018-04-30' AND '2018-5-27';")
data=cur.fetchall()
tanggalan=[]
for d in data:
    if d[1] not in tanggalan:
        tanggalan.append(d[1])
con.commit()
con.close()

dateList = []
enddate=100
for hari in range (0, enddate):
    weeklist=[]
    for perday in range(0,7):
        weeklist.append(a + datetime.timedelta(days = perday))
    a=(weeklist[-1] + datetime.timedelta(days=1))
    dateList.append(weeklist)
    if a not in tanggalan:
        break

#info : bentuk data : ID_STR, TANGGAL, KELAS MANUAL, KELAS LINEAR, KELAS POLY, KELAS RBF, KELAS SIG

indexx=16
x,y_pos,y_neg,xplot=svm.xypredic(indexx,dateList,data)
#svm.SVRtrain(x,y_pos,'linear_positive.sav')
#svm.SVRtrain(x,y_neg,'linear_negative.sav')

#//////////////////////////////////////////////////////////////////////////////

predict_pos,akurasi_pos=svm.SVRtest(x,y_pos,'linear_positive.sav')
predict_neg,akurasi_neg=svm.SVRtest(x,y_neg,'linear_negative_100.sav')


import matplotlib.pyplot as plt
plt.scatter(xplot, y_pos,color= 'black', label= 'Data')
plt.scatter(xplot, y_neg,color= 'green', label= 'Data')
plt.plot(xplot, predict_pos,color= 'black', label= ' model') # plotting the line made by the RBF kernel
plt.plot(xplot,predict_neg,color= 'green', label= 'Linear model') # plotting the line made by linear kernel
plt.xlabel('Week')
plt.ylabel('twit')
plt.title('Support Vector Regression')
plt.legend()
plt.show()