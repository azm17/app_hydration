# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:52:30 2019

@author: azumi
"""

import mysql.connector
import datetime

# データベースへの接続とカーソルの生成

server_host=''
server_port=0
user_name=''
user_pass=''
database_name=''
#database_name='hydration_db'

def kakunin(login_id,login_pass,port,host,db_name):
    global user_name
    global user_pass
    global server_port
    global server_host
    global database_name
    
    user_name = login_id
    user_pass = login_pass
    server_port = port
    server_host = host
    database_name = db_name
    
    user_name=login_id
    user_pass=login_pass
    conn = mysql.connector.connect(
        host = server_host,
        port = server_port,
        user = user_name,
        password = user_pass,
        database = database_name,
    )
    connected = conn.is_connected()
    print(connected)
    return connected
    
def sql_data_send(weight_after,weight_before,contents,time,moisture,tenki,shitsudo):
    data_list=[]
    conn = mysql.connector.connect(
        host = server_host,
        port = server_port,
        user = user_name,
        password = user_pass,
        database = database_name,
    )
    cur = conn.cursor()
    connected = conn.is_connected()
    
    if (not connected):
        conn.ping(True)
    
    tmp_day=datetime.date.today()
    day=tmp_day.strftime('%Y-%m-%d')
    cur.execute('''INSERT INTO `{}` (`day`, `weight_after`, `weight_before`, `contents`,`time`,`moisture`,`tenki`,`shitsudo`) 
                VALUES ('{}',{},{},'{}',{},{},{},{})'''.format(user_name,day,weight_after,weight_before,contents,time,moisture,tenki,shitsudo))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return  data_list

def sql_data_get(name):
    conn = mysql.connector.connect(
        host = server_host,
        port = server_port,
        user = user_name,
        password = user_pass,
        database = database_name,
    )
    cur = conn.cursor()
    connected = conn.is_connected()
    
    if (not connected):
        conn.ping(True)
    cur.execute('''SELECT * FROM `{}` '''.format(name))
    
    data_list=[]
    for row in cur.fetchall():
        #print(row)
        data_list.append(row)
    
    conn.commit()
    cur.close()
    conn.close()
    
    return  data_list

"""
ユーザー作成
１アカウントを作る
２テーブルを自分の名前で作る
CREATE TABLE `hydration_db`.`miyagawa` ( `day` DATE NOT NULL , `weight_after` FLOAT NOT NULL , `weight_before` FLOAT NOT NULL , `contents` TEXT NOT NULL , `time` FLOAT NOT NULL , `moisture` FLOAT NOT NULL, `tenki` FLOAT NOT NULL, `shitsudo` FLOAT NOT NULL ) ENGINE = InnoDB;
"""

#--Written By Mutsuyo-----------------------------------
def dassui_ritu(wb,wa):#脱水率
    z=round((wa-wb)/wb*100,1)#wb運動前　wa運動後
    return z

def hakkann_ritu(wb,wa,water,time):#1時間あたり発汗量
    z=round((wb-wa+water)/time,2)#water運動中飲水量ℓ　#time運動時間
    return z

def hakkann_ryo(wb,wa,water):#運動中発汗量(飲水必要量)
    z=round(wb-wa+water,2)
    return z

def hakkann_ritu_ex1(wb,water,time):#1時間あたり-1%発汗量
    z=round((wb-wb*0.99+water)/time,2)#water運動中飲水量ℓ　#time運動時間
    return z

def hakkann_ryo_ex1(wb,water):#運動時間あたり-1%発汗量(飲水必要量)
    z=round(wb-wb*0.99+water,2)#water運動中飲水量ℓ　#time運動時間
    return z

#--Written By Mutsuyo-----------------------------------
