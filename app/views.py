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


def classificationNameSELECT(request):
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


def classification(request, num):
    params = {}
    if(request.method == "POST"):
        method = request.POST["method"]
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        if(method == "SELECT1"):
            lim = request.POST["lim"]
            sql = "SELECT * FROM Genre ORDER BY date DESC LIMIT ?"
            box = []
            for i in cur.execute(sql, (lim,)):
                box.append([i[0], i[1], dt.strptime(
                    i[2], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"), i[3]])
            params = {
                "box": box,
            }
        elif(method == "SELECT2"):
            Id = request.POST["Id"]
            sql = "SELECT genre,date FROM Genre WHERE id = ?"
            box = []
            for i in cur.execute(sql, (Id,)):
                box.append(
                    [i[0], dt.strptime(i[1], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")])
            params = {
                "box": box,
            }
            print("C")
        elif(method == "INSERT" or method == "UPDATE"):
            genre = request.POST["genre"]
            date = dt.strptime(request.POST["date"], '%Y-%m-%d')
            if(method == "INSERT"):
                sql = "INSERT INTO Genre(genre,date,totalNumberOfActivity) VALUES(?,?,?)"
                cur.execute(sql, (genre, date, 0))
            elif(method == "UPDATE"):
                Id = request.POST["Id"]
                sql = "UPDATE Genre SET genre=?,date=?,totalNumberOfActivity=? WHERE id=?"
                cur.execute(sql, (genre, date, 0, Id))
            conn.commit()
        elif(method == "DELETE"):
            Id = request.POST["Id"]
            sql = "DELETE FROM Genre WHERE id = ?"
            cur.execute("PRAGMA foreign_keys=true")
            cur.execute(sql, (Id,))
            conn.commit()
        cur.close()
        conn.close()
    return JsonResponse(params)


def task(request, num):
    params = {}
    if(request.method == "POST"):
        box = []
        method = request.POST["method"]
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        if(method == "SELECT1"):
            lim = request.POST["lim"]
            sql = "SELECT Task.id,Task.task,Task.prior,Task.totalNumberOfActivity,Genre.genre,Task.date \
                FROM Task INNER JOIN Genre ON Task.genre_id = Genre.id ORDER BY Task.prior,Task.date DESC LIMIT ?"
            for i in cur.execute(sql, (lim,)):
                box.append([i[0], i[1], i[2], i[3], i[4], dt.strptime(
                    i[5], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")])
            params = {
                "box": box,
            }
        elif(method == "SELECT2"):
            sql = "SELECT genre FROM Genre"
            for i in cur.execute(sql):
                box.append([i[0]])
            params = {
                "box": box,
            }
        elif(method == "SELECT3"):
            Id = request.POST["Id"]
            sql = "SELECT Task.task,Task.prior,Genre.genre,Task.date FROM Task INNER JOIN Genre ON Genre.id = Task.genre_id WHERE Task.id = ?"
            for i in cur.execute(sql, (Id,)):
                box.append(
                    [i[0], priorChange(i[1]), i[2], dt.strptime(i[3], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")])
            params = {
                "box": box,
            }
        elif(method == "INSERT" or method == "UPDATE"):
            task = request.POST["task"]
            prior = priorChange(request.POST["prior"])
            genre_id = sqlGenre(request.POST["genre"])
            date = dt.strptime(request.POST["date"], '%Y-%m-%d')
            if(method == "INSERT"):
                sql = "INSERT INTO Task(task,prior,totalNumberOfActivity,genre_id,date) VALUES(?,?,?,?,?)"
                cur.execute(sql, (task, prior, 0, genre_id, date))
            elif(method == "UPDATE"):
                Id = request.POST["Id"]
                sql = "UPDATE Task SET task=?,prior=?,totalNumberOfActivity=?,genre_id=?,date=? WHERE id=?"
                cur.execute(sql, (task, prior, 0, genre_id, date, Id))
            conn.commit()
        elif(method == "DELETE"):
            Id = request.POST["Id"]
            sql = "DELETE FROM Task WHERE id = ?"
            cur.execute("PRAGMA foreign_keys=true")
            cur.execute("PRAGMA foreign_keys=true")
            cur.execute(sql, (Id,))
            conn.commit()
        cur.close()
        conn.close()
    return JsonResponse(params)


def taskNameSELECT2(request):
    conn = sql3.connect(dbname)
    cur = conn.cursor()
    sql = "SELECT task FROM Task"
    cur.execute(sql)
    params = {
        "box": cur.fetchall()
    }
    cur.close()
    conn.close()
    return JsonResponse(params)


def activity(request, txt, num):
    params = {}
    if(request.method == "POST"):
        box = []
        method = request.POST["method"]
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        if(method == "SELECT1"):
            lim = request.POST["lim"]
            task = txt
            if(task == "ALL"):
                sql = "SELECT Activity.id,Activity.date,Task.task,Activity.today,Activity.next FROM Activity INNER JOIN Task ON Activity.task_id = Task.id ORDER BY Activity.date DESC LIMIT ?"
                output = cur.execute(sql, (lim,))
            else:
                sql = "SELECT Activity.id,Activity.date,Task.task,Activity.today,Activity.next FROM Activity INNER JOIN Task ON Activity.task_id = Task.id WHERE Task.task = ? ORDER BY Activity.date DESC LIMIT ?"
                output = cur.execute(sql, (task, lim))
            for i in output:
                box.append([i[0], dt.strptime(
                    i[1], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"), i[2], i[3], i[4]])
            params = {
                "box": box,
            }
        elif(method == "SELECT2"):
            sql = "SELECT task FROM Task"
            for i in cur.execute(sql):
                box.append(i)
            params = {
                "box": box,
            }
        elif(method == "SELECT3"):
            Id = num
            sql = "SELECT Task.task,Activity.today,Activity.next,Activity.date FROM Activity INNER JOIN Task ON Task.id = Activity.task_id WHERE Activity.id=?"
            for i in cur.execute(sql, (Id,)):
                box.append([i[0], i[1], i[2], dt.strptime(
                    i[3], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")])
            params = {
                "box": box,
            }
            print(params)
        elif(method == "INSERT" or method == "UPDATE"):
            today = request.POST["today"]
            Next = request.POST["next"]
            date = dt.strptime(request.POST["date"], '%Y-%m-%d')
            sql = "SELECT id FROM Task WHERE task = ?"
            cur.execute(sql, (request.POST["task"],))
            task_id = cur.fetchall()[0][0]
            print(task_id)
            if(method == "INSERT"):
                sql = "INSERT INTO Activity(task_id,today,next,date) VALUES(?,?,?,?)"
                cur.execute(sql, (task_id, today, Next, date))
            elif(method == "UPDATE"):
                Id = request.POST["Id"]
                sql = "UPDATE Activity SET task_id=?,today=?,next=?,date=? WHERE id=?"
                cur.execute(sql, (task_id, today, Next, date, Id))
            conn.commit()
        elif(method == "DELETE"):
            Id = request.POST["Id"]
            sql = "DELETE FROM Activity WHERE id = ?"
            cur.execute("PRAGMA foreign_keys=true")
            cur.execute(sql, (Id,))
            conn.commit()
        cur.close()
        conn.close()

    return JsonResponse(params)
