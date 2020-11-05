import json
import random
import time
from calendar import timegm

import aiohttp
import asyncio
import aiomysql

from const import *

read_list = {}
open_users = []
write_list = []
task_list = []
notify_times = []

class User:
    """Пользователь"""
    def __init__(self, uid):
        """Загрузка пользователя"""
        self._id = uid


    async def get_timezone(self):
        """Возвращает часовой пояс в соответствии со списком, выдающимся
         при регистрации

        """
        try:
            data2 = await read_db(('select timezone from users where users'
                                       '.user=%s'), (str(self._id)))
        except Exception:
            write_list.append((self._id, DB_ERROR_USER))
            raise
        return data2[0]['timezone']

    async def get_reminders(self):
        """Возвращает список напоминаний пользователя"""
        try:
            prelist = await read_db(('select * from reminders where u'
                                            'ser=%s'), (str(self._id)))
        except Exception:
            write_list.append((self._id, DB_ERROR_USER))
            raise
        newlist = []
        for i in range(0, len(prelist)):
            newrem = Reminder(prelist[i]['id'], prelist[i]['user'], prelist[i]['text'], 
                                prelist[i]['time'], prelist[i]['repeattime'])
            newlist.append(newrem)
        self._reminders = newlist
        return self._reminders.copy()

    def sync_reminders(self):
        """Повторно планирует отправку напоминаний пользователя""" 
        for i in range(0, len(notify_times)):
            if notify_times[i]._user == self._id:
                notify_times[i] = None
        try:
            while True:
                notify_times.remove(None)
        except ValueError:
            pass
        for i in self._reminders: 
            notify_times.append(i)
        notify_times.sort(key=lambda b: b._time)

    async def change_timezone(self, tzid):
        """Изменяет часовой пояс пользователя

        Время напоминаний пользователя будет изменено в соответствии с 
        новым часовым поясом

        """
        try:
            lst = await read_db('select * from users where user=%s',
                                       (str(self._id)))
        except Exception:
            write_list.append((self._id, DB_ERROR_USER))
            raise
        prevtime = lst[0]['timezone']
        try:
            await write_db(('update users set timezone=%s where'
                                ' users.user=%s'), (str(tzid), str(self._id)))
        except Exception:
            write_list.append((self._id, DB_ERROR_USER))
            raise
        await self.get_reminders()
        for i in self._reminders:
            await i.edit(None, i._time + TIME_COR[int(tzid)] - TIME_COR[prevtime], 
                                                                        None)
        self.sync_reminders()

    async def add_reminder(self, text, time, repeattime):
        """Создает новое напоминание и планирует его отправку"""
        newrem = Reminder(None, self._id, text, time, repeattime)
        await newrem.write()
        await self.get_reminders()
        self.sync_reminders()

    async def edit_reminder(self, remindid, remindtext, timeremind, repeattime):
        """Редактирует напоминание и изменяет его копию, запланированную
         для отправки"""
        for i in range(0, len(self._reminders)):
            if self._reminders[i]._id == remindid:
                await self._reminders[i].edit(remindtext, timeremind, repeattime)
                for j in range(0, len(notify_times)):
                    if notify_times[j]._id == remindid:
                        notify_times[j] = self._reminders[i]
                        break
                break
        notify_times.sort(key=lambda b: b._time)

    async def del_reminder(self, ind):
        """Удаляет напоминание и отменяет его отправку"""
        for i in range(0, len(self._reminders)):
            if self._reminders[i]._id == ind:
                await self._reminders[i].delete()
                del self._reminders[i]
                break

    async def write(self, tz):
        """Регистрирует нового пользователя"""
        try:
            await write_db('insert into users(user, timezone) values (%s, %s)',
                                (str(self._id), str(tz)))
        except Exception:
            write_list.append((self._id, DB_ERROR_USER))
            raise
        pass
        

class Reminder:
    """Напоминание"""
    def __init__(self, uid, uuser, utext, utime, urepeattime):
        """Загрузка параметров напоминания"""
        self._user = uuser
        self._text = utext
        self._time = utime
        self._repeattime = urepeattime
        self._id = uid


    async def edit(self, remindtext, timeremind, repeattime):
        """Редактирует напоминание"""
        try:
            if remindtext:
                await write_db("update reminders set text = %s"
                                    " where reminders.id = %s", (remindtext, str(self._id)))
                self._text = remindtext
            if timeremind:
                await write_db("update reminders set time = %s"
                                    " where reminders.id = %s",
                                    (str(timeremind), str(self._id)))
                self._time = timeremind
            if not repeattime is None:
                await write_db("update reminders set repeattime = %s"
                                    " where reminders.id = %s",
                                    (str(repeattime), str(self._id)))
                self._repeattime = repeattime
        except Exception:
            write_list.append((self._user, DB_ERROR_USER))
            raise
        pass

    async def delete(self):
        """Удаляет напоминание из базы данных и отменяет его отправку.

        Копии напоминания, кроме той, что находтся в списке для отправки,
        не будут удалены

        """
        try:
            await write_db('delete from reminders where reminders.id = %s',
                                (str(self._id)))
        except Exception:
            write_list.append((self._user, DB_ERROR_USER))
            raise
        for i in range(0, len(notify_times)):
            if notify_times[i]._id == self._id:
                del notify_times[i]
                break

    async def write(self):
        """Сохранение нового напоминания"""
        try:
            await write_db("insert into `reminders` (`user`, `text`, `tim"+
                                "e`, `repeattime`) values (%s, %s, %s, %s)", 
                                (str(self._user), self._text, str(self._time),
                                 str(self._repeattime)))
        except Exception:
            write_list.append((self._user, DB_ERROR_USER))
            raise
        pass

    async def remind(self):
        """Отправка напоминания пользователю и планирование его повтора"""
        write_list.append((self._user, self._text))
        await asyncio.sleep(TIMEOUT)
        if self._repeattime and self._repeattime != 0:
            newrepeattime = self._repeattime
            if self._repeattime % (365*24*60*60) == 0:
                if (time.gmtime(self._time).tm_year + 1) % 1000 == 0:
                    newrepeattime = 366*self._repeattime/365
                elif (time.gmtime(self._time).tm_year + 1) % 100 == 0:
                    pass
                elif (time.gmtime(self._time).tm_year + 1) % 4 == 0:
                    newrepeattime = 366*self._repeattime/365
                else:
                    pass
            elif self._repeattime % (366*24*60*60) == 0:
                newrepeattime = 365*self._repeattime/366
            else:
                a = time.gmtime(self._time)
                b = time.gmtime(self._time+self._repeattime)
                if a.tm_mday == b.tm_mday and a.tm_hour == b.tm_hour \
                            and a.tm_min == b.tm_min and a.tm_sec == b.tm_sec:
                    mc = (b.tm_year-a.tm_year)*12+b.tm_mon-a.tm_mon
                    c = time.struct_time((b.tm_year, b.tm_mon+mc, b.tm_mday, 
                                            b.tm_hour, b.tm_min, b.tm_sec, 0,
                                            0, 0))
                    newrepeattime = timegm(c) - self._time - self._repeattime
            await self.edit(None, self._time + self._repeattime, newrepeattime)
            notify_times.sort(key=lambda b: b._time)
        else:
            await self.delete()
        await asyncio.sleep(TIMEOUT)

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return (await response.text())

async def login():
    """Вход в систему от имени сообщества"""
    global params
    try:
        res = await fetch(URL)
    except Exception:
        print("Вход в систему не удался.")
        raise
    res = json.loads(res)
    params = res['response']

async def fetch_read():
    """Функция получения сообщений пользователей

    Получает сообщения и складывает их в словарь read_list

    """
    while True:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        if msg['object']['message']['from_id'] not in read_list:
                            read_list[msg['object']['message']['from_id']] = []
                        read_list[msg['object']['message']['from_id']].append(msg['object']['message']['text'])
        except KeyError:
            await login()
        except Exception:
            print(READ_ERROR)
        for i in tuple(read_list):
            if i not in open_users and read_list[i] == []:
                del read_list[i]
        await asyncio.sleep(0.1)


async def fetch_write():
    """Функция отправки сообщений"""
    while True:
        while len(write_list) > 0:
            res = None
            while not res:
                try:
                    res = await fetch(MSG_URL.format(
                        user_id=write_list[0][0],
                        random_id=random.randint(100000000, 10000000000),
                        message = write_list[0][1]
                    ))
                except Exception:
                    print(WRITE_ERROR)
            del write_list[0]
            await asyncio.sleep(0.1)
        await asyncio.sleep(TIMEOUT)

async def open_db_conn():
    global pool
    pool = await aiomysql.create_pool(host='johnny.heliohost.org', 
        user='aterehov_System', password='Alexlevin123', db='aterehov_reminder')

async def read_db(cmd, args):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(cmd, args)
                a = await cur.fetchall()
        return a
    except Exception:
        print(DB_ERROR)
        raise

async def write_db(cmd, args):
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await conn.begin()
                await cur.execute(cmd, args)
                await conn.commit()
    except Exception:
        print(DB_ERROR)
        raise
    pass

async def task_manager():
    """Очистка памяти от завершившихся процессов"""
    while True:
        for i in range(0, len(task_list)):
            if task_list[i][1]._state == 'FINISHED':
                task_list[i] = None
        try:
            while True:
                task_list.remove(None)
        except ValueError:
            pass
        for i in range(0, len(open_users)):
            remover = 1
            for j in range(0, len(task_list)):
                if task_list[j][0] == open_users[i]:
                    remover = 0
                    break
            if remover == 1:
                open_users[i] = None
        try:
            while True:
                open_users.remove(None)
        except ValueError:
            pass
        await asyncio.sleep(TIMEOUT)


async def notifier():
    """Следит за временем и вовремя вызывает функции отправки напоминаний"""
    while True:
        if len(notify_times) != 0 and timegm(time.gmtime()) >= \
                                      notify_times[0]._time:
            await notify_times[0].remind()
        else:
            await asyncio.sleep(TIMEOUT)

async def update_notifications():
    """Загружает и планирует все напоминания из базы данных.

    Напоминания не будут скопированы в списки напоминаний пользователей

    """
    global notify_times
    prelist = await read_db('select * from reminders', None)
    newlist = []
    for i in range(0, len(prelist)):
        newrem = Reminder(prelist[i]['id'], prelist[i]['user'], prelist[i]['text'], 
                            prelist[i]['time'], prelist[i]['repeattime'])
        newlist.append(newrem)
    notify_times = newlist
    notify_times.sort(key=lambda b: b._time)