# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 17:14:23 2018

@author: user
"""

import MySQLdb
import datetime
import numpy as np
import random
con=MySQLdb.connect(host='127.0.0.1', port=3306, user='root', db='csv_db', charset='utf8')
cur=con.cursor()
cur.execute("SELECT * FROM dataset WHERE time_laps BETWEEN '2018-01-10' AND '2018-03-31';")
banyak=cur.fetchall()
semesta=[]
dbtanggal=[]
for ban in banyak:
    semesta.append(list(ban))
    if ban[1] not in dbtanggal:
        dbtanggal.append(ban[1])
con.commit
cur.close()

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
  
datamingguan=[]
for mingguan in dateList:
    seminggu=[]
    for sem in semesta:
        if sem[1] in mingguan:
            seminggu.append(sem)
    datamingguan.append(random.sample(seminggu,100))

            

