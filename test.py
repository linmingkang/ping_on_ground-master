# -*- coding: UTF-8 -*-
import os, time, pymysql, datetime

ping_interval = 3
db_user = ''
db_password = ''

try:
    file_r = open('/home/chsr/cf.d/groundusr.conf', 'r')
    file_r.readline()
    file_r.readline()
    db_user = file_r.readline()[len('mysqluser='):].strip()
    db_password = file_r.readline()[len('mysqlpasswd='):].strip()
    file_r.close()
except:
    print('配置文件groundusr.conf异常，该文件是否存在？该文件的内容格式是否符合规范？请相关人员检查。')
    exit()


db_host = '127.0.0.1'
db_port = 3306
db_name = 'db_ground_transfer'


def db_insert_update_del(cursor, sql):
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


try:
    db = pymysql.connect(
        host = db_host,
        port = db_port,
        user = db_user,
        password = db_password,
        db = db_name
    )
except:
    print('mysql数据库连接失败，请确保 /home/chsr/cf.d/trainuser.conf中数据库用户名、密码正确。\n程序退出')
    exit()

cursor = db.cursor()
train_id='SZGT10'
sql = "select * from train_connectivity where train_id='%s' and offline_time is null;" % train_id
cursor.execute(sql)
train_ip_lists = cursor.fetchall()
if train_ip_lists:
    print(train_ip_lists)
    aaa1=list(zip(*train_ip_lists))[2]
    print(aaa1[0])
    print(train_id in aaa1)
else:
    print("null")
