#!/usr/bin/env python
#coding=utf-8
import os
import sqlite3
import time

#全局变量，记录文件数目
global  file_number

# add database path
dbpath ='data/mydatabase.db'

#遍历disk磁盘
def all_files(disk):
    global  file_number
    print ("建立"+disk+"盘索引...")
    dir_path = disk
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    for root ,subdirs, files in os.walk(dir_path):
        for file in files:
            filefullpath = os.path.join(root,file)
            print ('file_path: '+filefullpath+'   file_name: '+file+"\n")
            #insert_to_db(filefullpath,file)
            cur.execute('INSERT INTO foo (o_id, file_path, file_name) VALUES(NULL, ?, ?)',[filefullpath.encode('utf-8').decode('utf-8'),file.encode('utf-8').decode('utf-8')])
            file_number += 1
    con.commit()
    print("file number is "+ str(file_number))
    print (disk+"盘索引建立完成")

#创建db
def create_db():
    sqlite_con = sqlite3.connect(dbpath)
    sqlite_cur = sqlite_con.cursor()
    sqlite_cur.execute('CREATE TABLE FOO (o_id INTEGER PRIMARY KEY, file_path VARCHAR(260), file_name VARCHAR(260))')
    sqlite_con.commit

#插入记录到db
def insert_to_db(file_path,file_name):
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    cur.execute('INSERT INTO foo (o_id, file_path, file_name) VALUES(NULL, ?, ?)',[file_path.decode(''),file_name.decode('utf-8')])
    con.commit()

#初始化数据
def InitDB():
    print ("开始建立文件索引，请等待...")
    global  file_number
    file_number = 0
    time_start = time.perf_counter()
    create_db()
    all_files('/')
    #all_files("d")
    #all_files("e")
    #all_files("f")
    time_end = time.perf_counter()
    print ("文件索引建立完毕！")
    print ("用时: "+str(time_end))
    print ("文件数: "+str(file_number))

#查找
def find_file(file_name):
    find_con = sqlite3.connect(dbpath)
    find_cur = find_con.cursor()
    bytesfile_name = file_name.encode('utf-8')
    find_cur.execute('SELECT * FROM FOO WHERE file_name = ?', [file_name.encode('utf-8').decode('gbk')])
    find_con.commit
    find_con.close
    print (find_cur.fetchall())


if __name__ == "__main__":
    if(os.path.exists(dbpath) == False):
        InitDB()
    while(1):
        find_file_name = input("输入要查找的文件名:")
        if(find_file_name == "#exit"):
            break
        find_file(find_file_name)
