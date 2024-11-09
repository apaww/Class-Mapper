import sqlite3
import os


DB_NAME='./data/database.db'


def createDatabase() -> None:
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Groups (             
        number      TEXT,
        name    TEXT ,        
        level      TEXT   ,        
        teacher TEXT    );''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Students (                
        surname      TEXT    ,
        name    TEXT ,        
        patronym      TEXT    ,        
        birth TEXT    ,
        sex TEXT ,
        ngroup TEXT ,
        nunion TEXT ,
        code TEXT,
        school TEXT ,
        parent TEXT,
        phone TEXT );''')
    conn.commit()
    conn.close()


def getGroups(filters):
    params = ''
    if filters is not None:
        params = filters
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    groups = cur.execute(
        f'''SELECT * FROM Groups
        {params}''')
    groups = list(groups)
    conn.close()
    return groups


def getStudents(filters):
    params = ''
    if filters is not None:
        params = filters
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    students = cur.execute(
        f'''SELECT * FROM Students
        {params}''')
    students = list(students)
    conn.close()
    return students


def getNumbers():
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    numbers = cur.execute(
        f'''SELECT number FROM Groups''')
    numbers = [number[0] for number in numbers]
    conn.close()
    return numbers


def getTeachers():
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    teachers = cur.execute(
        f'''SELECT teacher FROM Groups''')
    teachers = [teacher[0] for teacher in teachers]
    conn.close()
    return teachers


def getGroupNames():
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    names = cur.execute(
        f'''SELECT name FROM Groups''')
    names = [name[0] for name in names]
    conn.close()
    return names


def getDifficulties():
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    levels = cur.execute(
        f'''SELECT level FROM Groups''')
    levels = [level[0] for level in levels]
    conn.close()
    return levels


def addGroup(number, name, level, teacher):
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    cur.execute(
        f'''INSERT INTO Groups (number, name, level, teacher)
        VALUES(\'{number}\',\'{name}\',\'{level}\',\'{teacher}\')''')
    conn.commit()
    conn.close()


def editGroup(rowid, number, name, level, teacher):
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    cur.execute(
        f'''UPDATE Groups
        SET name=\'{name}\',
        level=\'{level}\',
        teacher=\'{teacher}\',
        number=\'{number}\'
        WHERE rowid=\'{rowid}\'''')
    conn.commit()
    conn.close()


def getGroup(rowid):
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    group = cur.execute(
        f'''SELECT * FROM Groups
        WHERE rowid=\'{rowid}\'''')
    print(f'SELECT REQUEST RESULT: {list(group)}') # debugging
    group = list(group)[0]
    conn.close()
    return group


def delGroups(first, last):
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    for i in range(first, last + 1):
        cur.execute(
            f'''DELETE FROM Groups
            WHERE rowid={i};''')
    cur.execute('''REINDEX Groups''')
    conn.commit()
    cur.execute('''VACUUM;''')
    conn.close()


def getSurnames():
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    surnames = cur.execute(
        f'''SELECT surname FROM Students''')
    surnames = [el[0] for el in surnames]
    conn.close()
    return surnames


def getNamesStudents():
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    names = cur.execute(
        f'''SELECT name FROM Students''')
    names = [el[0] for el in names]
    conn.close()
    return names


def getConnectedGroups():
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    data = cur.execute(
        f'''SELECT ngroup FROM Students''')
    data = [el[0] for el in data]
    conn.close()
    return data


def getConnectedUnions():
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    data = cur.execute(
        f'''SELECT nunion FROM Students''')
    data = [el[0] for el in data]
    conn.close()
    return data


def addStudent(surname, name, patronym, birth, sex, ngroup, nunion, code, school, parent, phone):
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    cur.execute(
        f'''INSERT INTO Students (surname, name, patronym, birth, sex, ngroup, nunion, code, school, parent, phone)
        VALUES(\'{surname}\',\'{name}\',\'{patronym}\',\'{birth}\',
        \'{sex}\',\'{ngroup}\',\'{nunion}\',\'{code}\',\'{school}\',\'{parent}\',\'{phone}\')''')
    conn.commit()
    conn.close()


def editStudent(rowid, surname, name, patronym, birth, sex, ngroup, nunion, code, school, parent, phone):
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    cur.execute(
        f'''UPDATE Students
        SET surname=\'{surname}\',
        name=\'{name}\',
        patronym=\'{patronym}\',
        birth=\'{birth}\',
        sex=\'{sex}\',
        ngroup=\'{ngroup}\',
        nunion=\'{nunion}\',
        school=\'{school}\',
        parent=\'{parent}\',
        phone=\'{phone}\',
        code=\'{code}\'
        WHERE rowid={rowid}''')
    conn.commit()
    conn.close()


def getStudent(rowid):
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    data = cur.execute(
        f'''SELECT * FROM Students
        WHERE rowid=\'{rowid}\'''')
    data = list(data)[0]
    conn.close()
    return data


def delStudents(first, last):
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    for i in range(first, last + 1):
        cur.execute(
            f'''DELETE FROM Students
            WHERE rowid={i};''')
    cur.execute('''REINDEX Students''')
    conn.commit()
    cur.execute('''VACUUM;''')
    conn.close()


def getCodes():
    conn: sqlite3.Connection = sqlite3.connect(DB_NAME)
    cur: sqlite3.Cursor = conn.cursor()
    data = cur.execute(
        f'''SELECT code FROM Students''')
    data = [el[0] for el in data]
    conn.close()
    return data