import pandas as pd
import pymysql.cursors
import datetime
import re
from config import *

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def open_con():
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='0000', database='tink', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    return connection, cursor

def close_con(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()

def data_file(name = 'data.xlsx'):
    return pd.read_excel(name)

def data_info():
    file = data_file()
    level = file['Опыт']
    sphere = file['Сфера']
    format = file['Формат']
    return sphere, level, format

def base_info(f = 0):
    file = data_file()
    comp = file['Компания']
    pos = file['Должность']
    net = file['Вилка']
    loc = file['Место работы']
    who = file['Кто ищет']
    des = file['Описание: html']
    id = file['id']
    if f == 1:
        return pos, comp, id
    else:
        return comp, pos, net, loc, who, des

def fvac(i):
    p, c, id = base_info(1)
    return p[i], c[i], id[i]

def fbase(i):
    c, p, n, l, w, d = base_info()
    return c[i], p[i], n[i], l[i], w[i], d[i]


# Подробнее
def more():
    return list(data_file()['Подробнее'])
# Id
def id():
    return list(data_file()['id'])


def fmore(i):
    return more()[i]
def fid(i):
    return id()[i]


# Vacancy number
def vac_number(more):
    return len(more)

# Vacancy number with filters
def vac_for_me(username):
    row = []
    data = unpack_sphere(username)
    sphere, level, format = data_info()
    for j in range(len(data)):
        for i in range(len(more())):
            if level[i] == get_level(username) and data[j] == sphere[i] and format[i] == get_format(username):
                row.append(i)
    return row

def unpack_sphere(username):
    result = []
    data = get_sphere(username)
    datad = list(data)
    data1 = get_sphere1(username)
    datad1 = list(data1)
    for i in range(len(datad)):
        if datad[i] == '1':
            result.append(jobs[i])
    for i in range(len(datad1)):
        if datad1[i] == '1':
            result.append(softs[i])
    return result



""" DataBase """
def create_user(username, chat_id):
    connection, cursor = open_con()
    sphere = '0' * len(jobs)
    sphere1 = '0' * len(softs)
    query = f"select * from users where username = '{username}'"
    cursor.execute(query)
    amount = cursor.rowcount
    if amount == 0:
        query = f"insert into users values ('{username}', '{chat_id}','{sphere}', NULL, NULL, NULL, 0, NULL, '{sphere1}')"
        cursor.execute(query)
        close_con(connection, cursor)
    else:
        close_con(connection, cursor)
        pass

def update_sphere(username, sphere):
    connection, cursor = open_con()
    query = f"update users set sphere = '{sphere}' where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)

def update_sphere1(username, sphere):
    connection, cursor = open_con()
    query = f"update users set sphere1 = '{sphere}' where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)

def get_sphere(username):
    connection, cursor = open_con()
    query = f"select sphere from users where username = '{username}'"
    cursor.execute(query)
    sphere = cursor.fetchone()['sphere']
    close_con(connection, cursor)
    return sphere

def get_sphere1(username):
    connection, cursor = open_con()
    query = f"select sphere1 from users where username = '{username}'"
    cursor.execute(query)
    sphere = cursor.fetchone()['sphere1']
    close_con(connection, cursor)
    return sphere

def update_salary(username, salary):
    connection, cursor = open_con()
    query = f"update users set net = '{salary}' where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)

def update_city(username, city):
    connection, cursor = open_con()
    query = f"update users set city = '{city}' where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)

def update_format(username, format):
    connection, cursor = open_con()
    query = f"update users set format = '{format}' where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)

def update_status(username):
    connection, cursor = open_con()
    query = f"update users set status = '1' where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)

def update_level(username, level):
    connection, cursor = open_con()
    query = f"update users set level = '{level}' where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)

def get_status(username):
    connection, cursor = open_con()
    query = f"select status from users where username = '{username}'"
    cursor.execute(query)
    status = cursor.fetchone()['status']
    close_con(connection, cursor)
    return status

def get_salary(username):
    connection, cursor = open_con()
    query = f"select net from users where username = '{username}'"
    cursor.execute(query)
    salary = cursor.fetchone()['net']
    close_con(connection, cursor)
    return salary

def get_location(username):
    connection, cursor = open_con()
    query = f"select city from users where username = '{username}'"
    cursor.execute(query)
    location = cursor.fetchone()['city']
    close_con(connection, cursor)
    return location

def get_level(username):
    connection, cursor = open_con()
    query = f"select level from users where username = '{username}'"
    cursor.execute(query)
    level = cursor.fetchone()['level']
    close_con(connection, cursor)
    return level

def get_format(username):
    connection, cursor = open_con()
    query = f"select format from users where username = '{username}'"
    cursor.execute(query)
    format = cursor.fetchone()['format']
    close_con(connection, cursor)
    return format


def update_vcs(username, i):
    vacancy = fmore(i)
    name, company, id = fvac(i)
    connection, cursor = open_con()
    ls = get_vacancies(username, 1)
    dtime = datetime.datetime.now()
    try:
        if vacancy not in ls:
            query = f"insert into vacancies values ('{username}','{id}','{name}','{company}', '{vacancy}','{dtime}')"
            cursor.execute(query)
            close_con(connection, cursor)
        else:
            close_con(connection, cursor)
            pass
    except:
        query = f"insert into vacancies values ('{username}','{id}','{name}', '{company}','{vacancy}','{dtime}')"
        cursor.execute(query)
        close_con(connection, cursor)

def create_log(username):
    connection, cursor = open_con()
    time = datetime.datetime.now()
    level = get_level(username)
    city = get_location(username)
    sphere = unpack_sphere(username)
    query = f'insert into logs values ("{time}", "{level}", "{city}", "{sphere}", "{username}")'
    cursor.execute(query)
    close_con(connection, cursor)


def get_names(username):
    connection, cursor = open_con()
    query = f"select name from vacancies where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)
    try:
        nms = []
        names = cursor.fetchall()
        for row in names:
            nms.append(str(row['name']))
        return nms
    except:
        return None


def get_times(username):
    connection, cursor = open_con()
    query = f"select dtime from vacancies where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)
    try:
        tms = []
        times = cursor.fetchall()
        for row in times:
            tms.append(str(row['dtime']).split(' ')[0])
            #print(tms)
        return tms
    except:
        return None

def get_cmps(username):
    connection, cursor = open_con()
    query = f"select company from vacancies where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)
    try:
        cmps = []
        companies = cursor.fetchall()
        for row in companies:
            cmps.append(str(row['company']))
        return cmps
    except:
        return None

def get_ids(username):
    connection, cursor = open_con()
    query = f"select id from vacancies where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)
    try:
        ids = []
        all_ids = cursor.fetchall()
        for row in all_ids:
            ids.append(str(row['id']))
        return ids
    except:
        return None

def delete_vac(username, id):
    connection, cursor = open_con()
    query = f"delete from vacancies where username = '{username}' and id = '{id}'"
    cursor.execute(query)
    close_con(connection, cursor)

def get_vacancies(username, flag):
    connection, cursor = open_con()
    nms = get_names(username)
    tms = get_times(username)
    cms = get_cmps(username)
    if nms is None:
        return None
    if tms is None:
        return None
    if cms is None:
        return None
    query = f"select vacancy from vacancies where username = '{username}'"
    cursor.execute(query)
    close_con(connection, cursor)
    try:
        i = 0
        vcs = ""
        vcs1 = []
        vacancies = cursor.fetchall()
        for row in vacancies:
            vcs1.append(str(row['vacancy']))
            vcs += '*' + str(i + 1) + '*' + '.\n' + "*Дата отклика:* " + str(tms[i]) + '\n' + "*Компания:* " + str(cms[i]) + '\n' + "*Должность:* " +  str(nms[i]) + '\n' + "*Контакты:* " + str(row['vacancy']) + '\n\n'
            i += 1
        if i == 0:
            return None
        if flag == 0:
            return vcs
        if flag == 1:
            return vcs1
    except:
        return None


def not_f(username):
    connection, cursor = open_con()
    time = datetime.datetime.now()
    query = f"insert into not_found values ('{username}', '{time}')"
    cursor.execute(query)
    close_con(connection, cursor)


def get_chats():
    connection, cursor = open_con()
    query = f"select chat_id from users"
    cursor.execute(query)
    close_con(connection, cursor)
    ls = []
    chats = cursor.fetchall()
    for row in chats:
        ls.append(str(row['chat_id']))
    return ls



""" Vacancy cards """
def card(vac):
    fc, fp, fn, fl, fw, fd = fbase(vac)
    fm = fmore(vac)
    return f'*Компания: *{fc}\n*Должность: *{fp}\n*Локация: *{fl}\n*Вилка: *{fn}\n\n*----------------  Кто ищет*\n{fw}\n\n*----------------  Описание*\n{fd}\n\n*Контакт:*\n{fm}'
