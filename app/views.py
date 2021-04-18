from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 as sql3
from datetime import datetime as dt

# 定義
dbname = "task.db"
msg = "Hello World"


def priorChange(tg):
    if(tg == 1):
        return "高い"
    elif(tg == 2):
        return "普通"
    elif(tg == 3):
        return "低い"
    elif(tg == 4):
        return "済み"
    elif(tg == "高い"):
        return 1
    elif(tg == "普通"):
        return 2
    elif(tg == "低い"):
        return 3
    elif(tg == "済み"):
        return 4


def sqlGenre(tg):
    conn = sql3.connect(dbname)
    cur = conn.cursor()
    sql = "SELECT id FROM Genre WHERE genre = ?"
    cur.execute(sql, (tg,))
    output = cur.fetchall()[0][0]
    cur.close()
    conn.close()
    return output


def sqlTask(tg):
    conn = sql3.connect(dbname)
    cur = conn.cursor()
    sql = "SELECT id FROM Task WHERE task = ?"
    cur.execute(sql, (tg,))
    output = cur.fetchall()[0][0]
    cur.close()
    conn.close()
    return output


def index(request):
    dbname = "task.db"
    conn = sql3.connect(dbname)
    cur = conn.cursor()
    sql = [
        "CREATE TABLE Genre(\
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
        genre TEXT NOT NULL UNIQUE,\
        date DATETIME NOT NULL,\
        totalNumberOfActivity INTEGER NOT NULL\
        )",
        "CREATE TABLE Task(\
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
        task TEXT NOT NULL UNIQUE,\
        prior INTEGER NOT NULL,\
        totalNumberOfActivity integter NOT NULL,\
        genre_id INTEGER NOT NULL,\
        date DATETIME NOT NULL,\
        FOREIGN KEY(genre_id) REFERENCES Genre(id) ON DELETE CASCADE\
        )",
        "CREATE TABLE Activity(\
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
        task_id INTEGER NOT NULL,\
        today TEXT NOT NULL,\
        next TEXT NOT NULL,\
        date DATETIME NOT NULL,\
        FOREIGN KEY(task_id) REFERENCES Task(id) ON DELETE CASCADE,\
        UNIQUE(task_id,date)\
        )",
    ]
    for i in range(len(sql)):
        try:
            cur.execute(sql[i])
        except:
            pass
    conn.commit()
    cur.close()
    conn.close()
    return render(request, "index.html")


def classificationInsert(request):
    if(request.method == "POST"):
        genre = request.POST["genre"]
        date = dt.strptime(request.POST["date"], '%Y-%m-%d')
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        sql = "INSERT INTO Genre(genre,date,totalNumberOfActivity) VALUES(?,?,0)"
        cur.execute(sql, (genre, date))
        conn.commit()
        params = {
            "": "",
        }
        cur.close()
        conn.close()
        return JsonResponse(params)
    return HttpResponse(msg)


def classificationSelect(request, num):
    if(request.method == "POST"):
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        sql = "SELECT * FROM Genre ORDER BY date DESC LIMIT 10"
        box = []
        for i in cur.execute(sql):
            box.append([i[0], i[1], dt.strptime(
                i[2], "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d"), i[3]])
        params = {
            "box": box,
        }
        cur.close()
        conn.close()
        return JsonResponse(params)
    return HttpResponse(msg)


def classificationNameSelect(request):
    if(request.method == "POST"):
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        sql = "SELECT genre FROM Genre ORDER BY date DESC"
        cur.execute(sql)
        params = {
            "box": cur.fetchall(),
        }
        cur.close()
        conn.close()
        return JsonResponse(params)
    return HttpResponse(msg)


def taskNameSelect(request, num):
    if(request.method == "POST"):
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        sql = "SELECT task FROM Task WHERE id = ?"
        cur.execute(sql, (num,))
        params = {
            "box": cur.fetchall(),
        }
        cur.close()
        conn.close()
        return JsonResponse(params)
    return HttpResponse(msg)


def taskInsert(request):
    if(request.method == "POST"):
        task = request.POST["task"]
        date = dt.strptime(request.POST["date"], '%Y-%m-%d')
        genre = sqlGenre(request.POST["genre"])
        prior = priorChange(request.POST["prior"])
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        print(genre)
        sql = "INSERT INTO Task(task,prior,totalNumberOfActivity,genre_id,date) VALUES(?,?,?,?,?)"
        cur.execute(sql, (task, prior, 0, genre, date))
        conn.commit()
        params = {
            "": "",
        }
        cur.close()
        conn.close()
        return JsonResponse(params)
    return HttpResponse(msg)


def taskSelect(request, num):
    if(request.method == "POST"):
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        sql = "SELECT Task.id,Task.task,Task.prior,Task.totalNumberOfActivity,Genre.genre,Task.date \
            FROM Task INNER JOIN Genre ON Task.genre_id = Genre.id ORDER BY prior LIMIT 10"
        box = []
        for i in cur.execute(sql):
            box.append([i[0], i[1], i[2], i[3], i[4], dt.strptime(
                i[5], "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d")])
        cur.execute(sql)
        params = {
            "box": box,
        }
        cur.close()
        conn.close()
        return JsonResponse(params)
    return HttpResponse(msg)


def activityInsert(request, num):
    if(request.method == "POST"):
        task_id = num
        today = request.POST["today"]
        Next = request.POST["next"]
        date = dt.strptime(request.POST["date"], '%Y-%m-%d')
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        sql = "INSERT INTO Activity(task_id,today,next,date) VALUES(?,?,?,?)"
        cur.execute(sql, (task_id, today, Next, date))
        conn.commit()
        params = {
            "": "",
        }
        cur.close()
        conn.close()
    return JsonResponse(params)


def activitySelect2(request, num):
    task_id = num
    conn = sql3.connect(dbname)
    cur = conn.cursor()
    sql = "SELECT Activity.id,Activity.date,Task.task,Activity.today,Activity.next FROM Activity INNER JOIN Task ON Activity.task_id = Task.id WHERE task_id = ? ORDER BY Activity.date DESC"
    box = []
    for i in cur.execute(sql, (task_id,)):
        box.append([i[0], dt.strptime(
            i[1], "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d"), i[2], i[3], i[4]])
    params = {
        "box": box,
    }
    cur.close()
    conn.close()
    return JsonResponse(params)


def taskNameSelect2(request):
    conn = sql3.connect(dbname)
    cur = conn.cursor()
    sql = "SELECT task FROM Task"
    cur.execute(sql)
    params = {
        "box":cur.fetchall()
    }
    cur.close()
    conn.close()
    return JsonResponse(params)


def activitySelect1(request):
    conn = sql3.connect(dbname)
    cur = conn.cursor()
    sql = "SELECT Activity.id,Activity.date,Task.task,Activity.today,Activity.next FROM Activity INNER JOIN Task ON Activity.task_id = Task.id"
    cur.execute(sql)
    box = []
    for i in cur.execute(sql):
        box.append([i[0], dt.strptime(
            i[1], "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d"), i[2], i[3], i[4]])
    params = {
        "box": box,
    }
    cur.close()
    conn.close()
    return JsonResponse(params)