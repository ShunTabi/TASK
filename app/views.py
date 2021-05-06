from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import sqlite3 as sql3
from datetime import datetime as dt


# 定義
dbname = "task.db"
msg = "Hello World"
color = ["#7fffd4", "#00ff7f", "#7cfc00", "#ffff00", "#ffd700", "#ff0000", "#ff1493",
         "#ffc0cb", "#ff00ff", "#9932cc", "#800080", "#4b0082", "#191970", "#0000ff", "#00ffff"]
plt.rcParams["font.family"] = "Yu Mincho"
mpl.use('Agg')


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
    sql = ["\
        CREATE TABLE Genre(\
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                genre TEXT NOT NULL UNIQUE,\
                    date DATETIME NOT NULL\
                        )", "\
        CREATE TABLE Task(\
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                task TEXT NOT NULL UNIQUE,\
                    prior INTEGER NOT NULL,\
                        genre_id INTEGER NOT NULL,\
                            date DATETIME NOT NULL,\
                                FOREIGN KEY(genre_id) REFERENCES Genre(id) ON DELETE CASCADE\
                                    )", "\
        CREATE TABLE Activity(\
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
        sql = "\
            SELECT genre \
                FROM Genre \
                    ORDER BY date DESC"
        cur.execute(sql)
        params = {
            "box": cur.fetchall(),
        }
        cur.close()
        conn.close()
        return JsonResponse(params)
    return HttpResponse(msg)


def classification(request, page):
    params = {}
    if(request.method == "POST"):
        method = request.POST["method"]
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        if(method == "SELECT1"):
            lim = request.POST["lim"]
            sql = "\
                SELECT Genre.id,Genre.genre,Genre.date,count(Genre.id) \
                    FROM Genre \
                        INNER JOIN Task \
                            ON Genre.id = Task.genre_id \
                                GROUP BY Genre.id \
                UNION \
                SELECT Genre.id,Genre.genre,Genre.date,0 \
                    FROM Genre \
                        WHERE Genre.id NOT IN(\
                            SELECT Genre.id \
                                FROM Genre \
                                    INNER JOIN Task \
                                        ON Genre.id = Task.genre_id \
                                            GROUP BY Genre.id \
                                                ) \
                ORDER BY Genre.date DESC \
                    LIMIT ? \
                        OFFSET ?"
            box = []
            for i in list(cur.execute(sql, (lim, (page-1)*int(lim)))):
                box.append([i[0], i[1], dt.strptime(
                    i[2], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"), i[3]])
            sql = "\
                SELECT Genre.id,Genre.date,count(Genre.id) \
                    FROM Genre \
                        INNER JOIN Task \
                            On Genre.id = Task.genre_id \
                                INNER JOIN Activity \
                                    On Task.id = Activity.task_id \
                                        GROUP BY Genre.id \
                UNION \
                SELECT Genre.id,Genre.date,0 \
                    FROM Genre \
                        WHERE Genre.id NOT IN( \
                            SELECT Genre.id \
                                FROM Genre \
                                    INNER JOIN Task \
                                        On Genre.id = Task.genre_id \
                                            INNER JOIN Activity \
                                                On Task.id = Activity.task_id \
                                                    GROUP BY Genre.id \
                                                        ) \
                ORDER BY Genre.date DESC \
                    LIMIT ? \
                        OFFSET ?"
            j = 0
            for i in list(cur.execute(sql, (lim, (page-1)*int(lim)))):
                box[j].append(i[2])
                j += 1
            sql = "\
                SELECT count(*) \
                    FROM Genre"
            cur.execute(sql)
            mx = cur.fetchall()[0][0]
            params = {
                "box": box,
                "mx": mx,
            }
        elif(method == "SELECT2"):
            Id = request.POST["Id"]
            sql = "\
                SELECT genre,date \
                    FROM Genre \
                        WHERE id = ?"
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
                sql = "\
                    INSERT INTO Genre(genre,date) VALUES(?,?)"
                cur.execute(sql, (genre, date))
            elif(method == "UPDATE"):
                Id = request.POST["Id"]
                sql = "\
                    UPDATE Genre \
                        SET genre=?,date=?\
                            WHERE id=?"
                cur.execute(sql, (genre, date, Id))
            conn.commit()
        elif(method == "DELETE"):
            Id = request.POST["Id"]
            sql = "\
                DELETE FROM Genre WHERE id = ?"
            cur.execute("PRAGMA foreign_keys=true")
            cur.execute(sql, (Id,))
            conn.commit()
        cur.close()
        conn.close()
    return JsonResponse(params)


def task(request, page):
    params = {}
    if(request.method == "POST"):
        box = []
        method = request.POST["method"]
        conn = sql3.connect(dbname)
        cur = conn.cursor()
        if(method == "SELECT1"):
            lim = request.POST["lim"]
            sql = "\
                SELECT Task.id,Task.task,Task.prior,count(Task.id),Genre.genre,Task.date \
                    FROM Task \
                        INNER JOIN Activity \
                            ON Task.id = Activity.task_id \
                                INNER JOIN Genre \
                                    ON Task.genre_id = Genre.id \
                                        GROUP BY Task.id \
                UNION \
                SELECT Task.id,Task.task,Task.prior,0,Genre.genre,Task.date \
                    FROM Task \
                        INNER JOIN Genre \
                            ON Task.genre_id = Genre.id \
                                WHERE Task.id NOT IN(\
                                    SELECT Task.id \
                                        FROM Task \
                                            INNER JOIN Activity \
                                                ON Task.id = Activity.task_id \
                                                    GROUP BY Task.id) \
                ORDER BY Task.prior,Task.date DESC \
                    LIMIT ? \
                        OFFSET ?"
            for i in cur.execute(sql, (lim, (page-1)*int(lim))):
                box.append([i[0], i[1], i[2], i[3], i[4], dt.strptime(
                    i[5], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")])
            sql = "\
                SELECT count(*) \
                    FROM task"
            cur.execute(sql)
            mx = cur.fetchall()[0][0]
            params = {
                "box": box,
                "mx": mx,
            }
        elif(method == "SELECT2"):
            sql = "\
                SELECT genre \
                    FROM Genre"
            for i in cur.execute(sql):
                box.append([i[0]])
            params = {
                "box": box,
            }
        elif(method == "SELECT3"):
            Id = request.POST["Id"]
            sql = "\
                SELECT Task.task,Task.prior,Genre.genre,Task.date\
                     FROM Task \
                         INNER JOIN Genre \
                             ON Genre.id = Task.genre_id \
                                 WHERE Task.id = ?"
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
                sql = "\
                    INSERT INTO Task(task,prior,genre_id,date) VALUES(?,?,?,?)"
                cur.execute(sql, (task, prior, genre_id, date))
            elif(method == "UPDATE"):
                Id = request.POST["Id"]
                sql = "\
                    UPDATE Task \
                        SET task=?,prior=?,genre_id=?,date=? \
                            WHERE id=?"
                cur.execute(sql, (task, prior, genre_id, date, Id))
            conn.commit()
        elif(method == "DELETE"):
            Id = request.POST["Id"]
            sql = "\
                DELETE FROM Task WHERE id = ?"
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
    sql = "\
        SELECT task \
            FROM Task"
    cur.execute(sql)
    params = {
        "box": cur.fetchall()
    }
    cur.close()
    conn.close()
    return JsonResponse(params)


def activity(request, txt, page):
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
                sql = "\
                    SELECT count(*) \
                        FROM Activity"
                cur.execute(sql)
                mx = cur.fetchall()[0]
                sql = "\
                    SELECT Activity.id,Activity.date,Task.task,Activity.today,Activity.next \
                        FROM Activity INNER \
                            JOIN Task \
                                ON Activity.task_id = Task.id \
                                    ORDER BY Activity.date DESC \
                                        LIMIT ? \
                                            OFFSET ?"
                output = cur.execute(sql, (lim, (page-1)*int(lim)))
            else:
                sql = "\
                    SELECT count(*) \
                        FROM Activity \
                            INNER JOIN Task \
                                ON Task.id = Activity.task_id \
                                    WHERE Task.task = ?"
                cur.execute(sql, (txt,))
                mx = cur.fetchall()[0]
                sql = "\
                    SELECT Activity.id,Activity.date,Task.task,Activity.today,Activity.next \
                        FROM Activity \
                            INNER JOIN Task \
                                ON Activity.task_id = Task.id \
                                    WHERE Task.task = ? \
                                        ORDER BY Activity.date DESC \
                                            LIMIT ? \
                                                OFFSET ?"
                output = cur.execute(sql, (task, lim, (page-1)*int(lim)))
            for i in output:
                box.append([i[0], dt.strptime(
                    i[1], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"), i[2], i[3], i[4]])
            params = {
                "box": box,
                "mx": mx,
            }
        elif(method == "SELECT2"):
            sql = "\
                SELECT task \
                    FROM Task"
            for i in cur.execute(sql):
                box.append(i)
            params = {
                "box": box,
            }
        elif(method == "SELECT3"):
            Id = page
            sql = "\
                SELECT Task.task,Activity.today,Activity.next,Activity.date \
                    FROM Activity \
                        INNER JOIN Task \
                            ON Task.id = Activity.task_id \
                                WHERE Activity.id=?"
            for i in cur.execute(sql, (Id,)):
                box.append([i[0], i[1], i[2], dt.strptime(
                    i[3], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")])
            params = {
                "box": box,
            }
        elif(method == "INSERT" or method == "UPDATE"):
            today = request.POST["today"]
            Next = request.POST["next"]
            date = dt.strptime(request.POST["date"], '%Y-%m-%d')
            sql = "\
                SELECT id \
                    FROM Task \
                        WHERE task = ?"
            cur.execute(sql, (request.POST["task"],))
            task_id = cur.fetchall()[0][0]
            if(method == "INSERT"):
                sql = "\
                    INSERT INTO Activity(task_id,today,next,date) VALUES(?,?,?,?)"
                cur.execute(sql, (task_id, today, Next, date))
            elif(method == "UPDATE"):
                Id = request.POST["Id"]
                sql = "\
                    UPDATE Activity \
                        SET task_id=?,today=?,next=?,date=? \
                            WHERE id=?"
                cur.execute(sql, (task_id, today, Next, date, Id))
            conn.commit()
        elif(method == "DELETE"):
            Id = request.POST["Id"]
            sql = "\
                DELETE FROM Activity \
                    WHERE id = ?"
            cur.execute("PRAGMA foreign_keys=true")
            cur.execute(sql, (Id,))
            conn.commit()
        cur.close()
        conn.close()
    return JsonResponse(params)


def Graph(request):
    conn = sql3.connect(dbname)
    cur = conn.cursor()
    sql = "\
        SELECT Task.id,Task.task,strftime('%Y-%m',Activity.date) AS date,count(Task.id) \
            FROM Task \
                INNER JOIN Activity \
                    ON Task.id = Activity.task_id \
                        GROUP BY strftime('%Y-%m',Activity.date),Task_id"
    box = list(cur.execute(sql))
    cur.close()
    conn.close()
    df = pd.DataFrame(box).set_index(2)
    df.columns = ["id", "task", "num"]
    tName = list(set(df["task"]))
    tg1 = pd.DataFrame()
    for i in range(len(tName)):
        tg = df[df["task"] == tName[i]]["num"]
        if(i == 0):
            tg1 = tg
        else:
            tg1 = pd.concat([tg1, tg], axis=1)
    tg1 = tg1.fillna(0).sort_index()
    tg1.columns = tName
    plt.figure(figsize=(10, 5))
    sns.set_palette('pastel')
    # sns.set_palette('rocket')
    x = tg1.index
    for i in range(len(tName)):
        tg = tName[i]
        plt.bar(x, tg1[tName[i]], label=tg,
                bottom=tg1[tg1.columns[0:i]].sum(axis=1))
    plt.xlabel("Date", fontsize=11)
    plt.ylabel("Activity", fontsize=11)
    plt.legend(loc="upper left", fontsize=11)
    File = r'E:\desktop\task\app\static\output.png'
    plt.savefig(File)
    return HttpResponse("Hello")
