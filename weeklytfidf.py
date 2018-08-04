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

import MySQLdb
import datetime
import pandas as pd
import maintfidf as mf
import SVMfull as svm

#Access DataBase


a= datetime.datetime.strptime("2018-05-25","%Y-%m-%d").date()
con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='1000an', charset='utf8')
cur=con.cursor()
cur.execute("""SELECT * from dataset WHERE time_laps BETWEEN '2018-05-25' AND '2018-05-31';""")
banyak=cur.fetchall()
semesta=[]
stopword=[]
dbtanggal=[]
for ban in banyak:
    semesta.append(list(ban))
    if ban[1] not in dbtanggal:
        dbtanggal.append(ban[1])

con.commit()
cur.close()
#Close DataBase


dateList = []
enddate=7
for hari in range (0, enddate):
#    for perday in range(0,7):
    dateList.append(a + datetime.timedelta(days = hari))


tfidf=mf.fulltfidf(dateList,semesta)
datasvm=pd.DataFrame(tfidf)

# SVM Begin
svm_linear='svm-minggu.sav'

x,y=svm.SVCxy(tfidf,datasvm)
svm.SVCtrain(x,y,svm_linear)

framey_lin=svm.SVCtest(x,y,svm_linear)


#save data to db
con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='csv_db', charset='utf8')
cur=con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS simulasi (id_str varchar(18), tanggal date, text varchar(153), class_manual varchar(8), class_linear varchar(8), PRIMARY KEY(id_str));")
eksekution="INSERT INTO simulasi VALUES (%s, %s, %s, %s, %s);"
to_db=[(z[0][0], z[0][1], z[0][5], z[0][4], z[1])for z in zip(tfidf, framey_lin)]
cur.executemany(eksekution,to_db)
con.commit()
con.close()
