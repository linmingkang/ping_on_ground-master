# -*- coding: UTF-8 -*-
import os, time, pymysql, datetime


ping_interval = 2
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
cursor.execute('select train_id, train_ip from train_ip;')
train_ip_lists = cursor.fetchall()
if len(train_ip_lists) == 0:
    print('mysql数据库中的train_ip数据表为空，请相关人员进行填写，将火车id和ip填入数据表trian_ip中。如果你不懂我在说什么，请查阅《车地传输项目与传输软件接口协议》进行学习。\n程序退出')
    exit()
train_ips = {}
last_ping = {}
online_time = {}
for train_ip in train_ip_lists:
    train_ips[train_ip[0]] = train_ip[1]
    last_ping[train_ip[0]] = 0
    online_time[train_ip[0]] = ''
sql = 'delete from train_online_flag'
db_insert_update_del(cursor, sql)
for train_id, train_ip in train_ips.items():
    sql = "insert into train_online_flag(train_id, online_flag) values('%s', 0);" % train_id
    db_insert_update_del(cursor, sql)


while True:
    for train_id, train_ip in train_ips.items():
        ping_res = os.popen('ping -c 1 -w 1 %s' % train_ip).read()
        ping = 0
        if '1 received' in ping_res:
            ping = 1
        if ping == 0:   # pingbutong
            sql = "update train_online_flag set online_flag = 0 where train_id = '%s';" % train_id
            db_insert_update_del(cursor, sql)
            if ping != last_ping[train_id]:
                off = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql = "delete from train_connectivity where train_id='%s' and offline_time is null;" % train_id
                db_insert_update_del(cursor, sql)
                sql = "insert into train_connectivity(train_id, online_time, offline_time) values('%s', '%s', '%s');" % (train_id, online_time[train_id], off)
                db_insert_update_del(cursor, sql)
            else:
                cursor = db.cursor()
                sql = "select * from train_connectivity where train_id='%s' and offline_time is null;" % train_id
                cursor.execute(sql)
                old_data = cursor.fetchall()
                if old_data:
                    old_data1 = list(zip(*old_data))[2]
                    online_time[train_id] = old_data1[0]
                    off = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sql = "delete from train_connectivity where train_id='%s' and offline_time is null;" % train_id
                    db_insert_update_del(cursor, sql)
                    sql = "insert into train_connectivity(train_id, online_time, offline_time) values('%s', '%s', '%s');" % (train_id, online_time[train_id], off)
                    db_insert_update_del(cursor, sql)
        else:   # pingtong
            sql = "update train_online_flag set online_flag = 1 where train_id = '%s';" % train_id
            db_insert_update_del(cursor, sql)
            if ping != last_ping[train_id]:
                cursor = db.cursor()
                sql = "select * from train_connectivity where train_id='%s' and offline_time is null;" % train_id
                cursor.execute(sql)
                old_data = cursor.fetchall()
                if old_data:
                    old_data1 = list(zip(*old_data))[2]
                    online_time[train_id] = old_data1[0]
                else:
                    online_time[train_id] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sql = "insert into train_connectivity(train_id, online_time) values('%s', '%s');" % (train_id, online_time[train_id])
                    db_insert_update_del(cursor, sql)
        last_ping[train_id] = ping
    cursor = db.cursor()
    cursor.execute('select train_id, train_ip from train_ip;')
    aaa = cursor.fetchall()
    aaa1=list(zip(*aaa))[0]
    for b in list(train_ips):
        if b not in aaa1:
            train_ips.pop(b)
            last_ping.pop(b)
            online_time.pop(b)
            sql = "delete from train_online_flag where train_id = '%s'" %b
            db_insert_update_del(cursor, sql)
    for a in aaa:
        if a[0] not in train_ips:
            train_ips[a[0]] = a[1]
            last_ping[a[0]] = 0
            online_time[a[0]] = ''
            sql = "insert into train_online_flag(train_id, online_flag) values('%s', 0);" % a[0]
            db_insert_update_del(cursor, sql)
    time.sleep(ping_interval)
db.close()

