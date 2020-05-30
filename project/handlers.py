#import aiohttp
import random
import time
import json
import asyncio

from sqlalchemy import create_engine
from const import *
from utils import *

notifytimes = []
users = []

class user:
    global notifytimes
    __id = None
    __reminders = None
    def gettimezone(self):
        connection = engine.connect()
        data = connection.execute('select timezone from users where users.user='+str(self.__id))
        connection.close()
        data2 = data.next()
        return data2[0]
    def __init__(self, uid):
        self.__id = uid
    def getid(self):
        return self.__id
    def getreminders(self, reload):
        if reload:
            connection = engine.connect()
            newdata = connection.execute('select * from reminders where user='+str(self.__id))
            connection.close()
            prelist = []
            try:
                while True:
                    prelist.append(newdata.next())
            except StopIteration:
                pass
            for i in range(0, len(prelist)):
                prelist[i] = list(prelist[i])
            newlist = []
            for i in range(0, len(prelist)):
                newrem = reminder(prelist[i][0], prelist[i][1], prelist[i][2], prelist[i][3], prelist[i][4])
                # newlist.append([])
                # newlist[i].append(prelist[i][0])
                # newlist[i].append(prelist[i][3])
                # newlist[i].append(prelist[i][4])
                # newlist[i].append(prelist[i][2])
                # newlist[i].append(prelist[i][1])
                newlist.append(newrem)
            self.__reminders = newlist
        #reminders.sort()
        return self.__reminders.copy()
    def syncreminders(self, reminders):
        for i in range(0, len(notifytimes)):
            if notifytimes[i].getuser() == self.__id:
                notifytimes[i] = None
        try:
            while True:
                notifytimes.remove(None)
        except ValueError:
            pass
        for i in reminders: 
            notifytimes.append(i)
        notifytimes.sort(key=lambda b: b.gettime())
    def changetimezone(self, tzid):
        connection = engine.connect()
        data = connection.execute('select * from users where user='+str(self.__id))
        connection.close()
        lst = []
        lst.append(data.next())
        prevtime = lst[0][2]
        userid = lst[0][0]
        connection = engine.connect()
        trans = connection.begin()
        connection.execute('update users set timezone='+str(tzid)+' where users.id='+str(userid))
        trans.commit()
        connection.close()
        upd = False
        if self.__reminders == None:
            upd = True
        self.getreminders(upd)
        for i in self.__reminders:
            i.edit(None, i.gettime() + timecor[int(tzid)] - timecor[prevtime], None)
        # connection = engine.connect()
        # remindersdata = connection.execute('select * from reminders where reminders.user='+str(self.__id))
        # connection.close()
        # reminderslist = []
        # try:
        #     while True:
        #         reminderslist.append(remindersdata.next())
        # except StopIteration:
        #     pass
        # connection = engine.connect()
        # trans = connection.begin()
        # for i in reminderslist:
        #     connection.execute('update reminders set time='+str(i[3]-timecor[prevtime]+timecor[int(tzid)])+' where reminders.id='+str(i[0]))
        # trans.commit()
        # connection.close()
        # #def func(users):
        # #    fl = open('users.db', 'w')
        # #    fl.write("\n".join(users))
        # #    fl.close()
        # #filequeue.append([func, users])
        # a = user.getreminders(self, True)
        # user.syncreminders(self, a)
        self.syncreminders(self.__reminders)
    def addreminder(self, text, time, repeattime):
        newrem = reminder(None, self.__id, text, time, repeattime)
        newrem.write()
        self.getreminders(True)
        self.syncreminders(self.__reminders)
        # connection = engine.connect()
        # trans = connection.begin()
        # connection.execute("insert into `reminders` (`user`, `text`, `time`, `repeattime`) values ('"+str(self.__id)+"', '"+text+"', '"+str(time)+"', '"+str(repeattime)+"')")
        # trans.commit()
        # connection.close()
        # a = user.getreminders(self, True)
        # user.syncreminders(self, a)
    def editreminder(self, remindid, remindtext, timeremind, repeattime):
        for i in self.__reminders:
            if i.getid() == remindid:
                i.edit(remindtext, timeremind, repeattime)
                break
        # connection = engine.connect()
        # trans = connection.begin()
        # if remindtext:
        #     connection.execute("update reminders set text = '"+remindtext+"' where reminders.id = "+str(remindid))
        # if timeremind:
        #     connection.execute("update reminders set time = '"+str(timeremind)+"' where reminders.id = "+str(remindid))
        # if repeattime:
        #     connection.execute("update reminders set repeattime = '"+str(repeattime)+"' where reminders.id = "+str(remindid))
        # trans.commit()
        # connection.close()
        # a = user.getreminders(True)
        self.syncreminders(self.__reminders)
    def delreminder(self, ind):
        connection = engine.connect()
        trans = connection.begin()
        connection.execute('delete from reminders where reminders.id = '+str(ind))
        trans.commit()
        connection.close()
        #users = reloaduserdb()
        #ind = users.index('~'+lst[no])
        #del users[ind]
        #del users[ind]
        #del users[ind]
        #def func(users):
        #    fl = open('users.db', 'w')
        #    fl.write("\n".join(users))
        #    fl.close()
        #filequeue.append([func, users])
        a = user.getreminders(self, True)
        user.syncreminders(self, a)
    def write(self, tz):
        connection = engine.connect()
        trans = connection.begin()
        connection.execute('insert into users(user, timezone) values ('+str(self.__id)+', '+str(tz)+')')
        trans.commit()
        connection.close()
        

class reminder:
    global notifytimes
    __id = None
    __user = None
    __text = None
    __time = None
    __repeattime = None
    def __init__(self, uid, uuser, utext, utime, urepeattime):
        self.__user = uuser
        self.__text = utext
        self.__time = utime
        self.__repeattime = urepeattime
        self.__id = uid
    def getid(self):
        return self.__id
    def getuser(self):
        return self.__user
    def gettext(self):
        return self.__text
    def gettime(self):
        return self.__time
    def getrepeattime(self):
        return self.__repeattime
    def edit(self, remindtext, timeremind, repeattime):
        connection = engine.connect()
        trans = connection.begin()
        if remindtext:
            connection.execute("update reminders set text = '"+remindtext+"' where reminders.id = "+str(self.__id))
            self.__text = remindtext
        if timeremind:
            connection.execute("update reminders set time = '"+str(timeremind)+"' where reminders.id = "+str(self.__id))
            self.__time = timeremind
        if repeattime != None:
            connection.execute("update reminders set repeattime = '"+str(repeattime)+"' where reminders.id = "+str(self.__id))
            self.__repeattime = repeattime
        trans.commit()
        connection.close()
    def delete(self):
        connection = engine.connect()
        trans = connection.begin()
        connection.execute('delete from reminders where reminders.id = '+str(self.__id))
        trans.commit()
        connection.close()
        del self
    def write(self):
        connection = engine.connect()
        trans = connection.begin()
        connection.execute("insert into `reminders` (`user`, `text`, `time`, `repeattime`) values ('"+str(self.__user)+"', '"+self.__text+"', '"+str(self.__time)+"', '"+str(self.__repeattime)+"')")
        trans.commit()
        connection.close()
    async def remind(self):
        res = await fetch(MSG_URL.format(
            user_id=self.__user,
            random_id=random.randint(100000000, 10000000000),
            message = self.__text
        ))
        print(res)
        if self.__repeattime and self.__repeattime != 0:
            self.edit(None, self.__time + self.__repeattime, None)
            notifytimes.sort(key=lambda b: b.gettime())
        else:
            self.delete()




    
tasklist = []
openusers = []
filequeue = []
engine = create_engine('mysql://aterehov:Alexlevin123@johnny.heliohost.org/aterehov_reminder?charset=utf8',  pool_size=10, max_overflow=20, echo=True)
#connection = engine.connect()
#async def filewriter():
#    global filequeue
#    while True:
#        for i in range(0, len(filequeue)):
#            filequeue[i][0](filequeue[i][1])
#            filequeue[i] = None
#        try:
#            while True:
#                filequeue.remove(None)
#        except:
#            pass
#        await asyncio.sleep(1)
async def taskmanager():
    global tasklist
    while True:
        for i in range(0, len(tasklist)):
            if tasklist[i][1]._state == 'FINISHED':
                tasklist[i] = None
        try:
            while True:
                tasklist.remove(None)
        except ValueError:
            pass
        for i in range(0, len(openusers)):
            remover = 1
            for j in range(0, len(tasklist)):
                if tasklist[j][0] == openusers[i]:
                    remover = 0
                    break
            if remover == 1:
                openusers[i] = None
        try:
            while True:
                openusers.remove(None)
        except ValueError:
            pass
        await asyncio.sleep(1)
async def notifier():
    global notifytimes
    while True:
        if len(notifytimes) != 0 and time.mktime(time.localtime()) >= notifytimes[0].gettime():
            notifytimes[0].remind()
        else:
            await asyncio.sleep(1)


def updatenotifications():
    global notifytimes
    connection = engine.connect()
    newdata = connection.execute('select * from reminders')
    connection.close()
    prelist = []
    try:
        while True:
            prelist.append(newdata.next())
    except StopIteration:
        pass
    for i in range(0, len(prelist)):
        prelist[i] = list(prelist[i])
    #for i in range(0, len(prelist)):
    #    del prelist[i][0]
    newlist = []
    for i in range(0, len(prelist)):
        newrem = reminder(prelist[i][0], prelist[i][1], prelist[i][2], prelist[i][3], prelist[i][4])
        # newlist.append([])
        # newlist[i].append(prelist[i][0])
        # newlist[i].append(prelist[i][3])
        # newlist[i].append(prelist[i][4])
        # newlist[i].append(prelist[i][2])
        # newlist[i].append(prelist[i][1])
        newlist.append(newrem)
    notifytimes = newlist
    # users = reloaduserdb()
    # notifytimes = []
    # for i in range(0, len(users)):
    #     if len(users[i]) == 0:
    #         pass
    #     elif users[i][0] == '#':
    #         userindex = i
    #     elif users[i][0] == '~':
    #         notifytimes.append([float(users[i+1]), float(users[i+2]), users[i][1:], users[userindex][1:]])
    notifytimes.sort(key=lambda b: b.gettime())





async def mainwindow(user, params):
    global tasklist
    res = await fetch(MSG_URL.format(
        user_id=user.getid(),
        random_id=random.randint(100000000, 10000000000),
        message=mainwindowtext
    ))
    print(res)
    flag = 0
    while flag == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            if msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '1':
                                tasklist.append([msg['object']['message']['from_id'], asyncio.gather(changetime(user, params.copy()))])
                                flag = 1
                            elif msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '2':
                                tasklist.append([msg['object']['message']['from_id'], asyncio.gather(addreminder(user, params.copy()))])
                                flag = 1
                            elif msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '3':
                                tasklist.append([msg['object']['message']['from_id'], asyncio.gather(viewreminders(user, params.copy()))])
                                flag = 1
                            elif msg['object']['message']['from_id'] == user.getid():
                                tasklist.append([msg['object']['message']['from_id'], asyncio.gather(wronganswer(user))])
                        except:
                            tasklist.append([msg['object']['message']['from_id'], asyncio.gather(wronganswer(user))])
        except:
            raise
    await asyncio.sleep(1)


async def changetime(user, params):
    message=changetimetext
    message = message.split('\n')
    for i in message:
        res = await fetch(MSG_URL.format(
            user_id=user.getid(),
            random_id=random.randint(100000000, 10000000000),
            message = i))
        print(res)
        await asyncio.sleep(0.2)
    flag = 0
    while flag == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            if msg['object']['message']['from_id'] == user.getid() and 1 <= int(msg['object']['message']['text']) <= 36:
                                user.changetimezone(int(msg['object']['message']['text']))
                                # connection = engine.connect()
                                # data = connection.execute('select * from users where user='+str(msg['object']['message']['from_id']))
                                # connection.close()
                                # lst = []
                                # lst.append(data.next())
                                # prevtime = lst[0][2]
                                # userid = lst[0][0]
                                # connection = engine.connect()
                                # trans = connection.begin()
                                # connection.execute('update users set timezone='+str(msg['object']['message']['text'])+' where users.id='+str(userid))
                                # trans.commit()
                                # connection.close()
                                # #users = reloaduserdb()
                                # #ind = users.index('#' + str(msg['object']['message']['from_id']))
                                # #prevtime = int(users[ind+1])
                                # #users[ind+1] = msg['object']['message']['text']
                                # #ind += 2
                                # #nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                                # #while ind < len(users)-1 and users[ind][0] != \
                                # #        '#':
                                # #    try:
                                # #        if int(users[ind][0]) in nums and users\
                                # #                [ind-2][0] != '~':
                                # #            users[ind] = str(float(users[ind]) \
                                # #                             - timecor[prevtime]\
                                # #                             + timecor[int(msg\
                                # #                              ['object']\
                                # #                            ['message']\
                                # #                            ['text'])])
                                # #    except:
                                # #        pass
                                # #    ind += 1
                                # connection = engine.connect()
                                # remindersdata = connection.execute('select * from reminders where user='+str(msg['object']['message']['from_id']))
                                # reminderslist = []
                                # try:
                                #     while True:
                                #         reminderslist.append(remindersdata.next())
                                # except StopIteration:
                                #     pass
                                # trans = connection.begin()
                                # for i in reminderslist:
                                #     connection.execute('update reminders set time='+str(i[3]-timecor[prevtime]+timecor[int(msg['object']['message']['text'])])+' where reminders.id='+str(i[0]))
                                # trans.commit()
                                # connection.close()
                                # #def func(users):
                                # #    fl = open('users.db', 'w')
                                # #    fl.write("\n".join(users))
                                # #    fl.close()
                                # #filequeue.append([func, users])
                                # updatenotifications()
                                flag = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=user.getid(),
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message=edittimetext
                                    ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid() and int(msg['object']['message']['text']) == 0:
                                flag = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=user.getid(),
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = continuetext
                                    ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid():
                                tasklist.append([msg['object']['message']['from_id'], asyncio.gather(wronganswer(user))])
                                await asyncio.sleep(0.2)
                        except ValueError:
                            tasklist.append([msg['object']['message']['from_id'], asyncio.gather(wronganswer(user))])
                            await asyncio.sleep(0.2)
        except:
            raise
    await asyncio.sleep(0.2)
async def addreminder(user, params):
    res = await fetch(MSG_URL.format(
        user_id=user.getid(),
        random_id=random.randint(100000000, 10000000000),
        message = addreminderentertext
    ))
    print(res)
    #await asyncio.sleep(0.2)
    flag = 0
    stop = 0
    while flag == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            if msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '0':
                                flag = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']['from_id'],
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = continuetext
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                                stop = 1
                            elif msg['object']['message']['from_id'] == user.getid():
                                try:
                                    if msg['object']['message']['text'][0] == \
                                            '#' or msg['object']['message']\
                                            ['text'][0] == ' ' or 0 <= int(msg\
                                            ['object']['message']['text'][0]) \
                                            <= 9:
                                        res = await fetch(MSG_URL.format(
                                            user_id=user.getid(),
                                            random_id=random.randint(100000000,
                                                                     10000000000),
                                            message = addreminderwrongtext
                                        ))
                                        print(res)
                                        await asyncio.sleep(0.2)
                                    
                                        
                                except ValueError:
                                    remindtext = msg['object']['message']\
                                        ['text']
                                    flag = 1
                                    res = await fetch(MSG_URL.format(
                                        user_id=user.getid(),
                                        random_id=random.randint(100000000,
                                                                 10000000000),
                                        message = addreminderentertime
                                    ))
                                    print(res)
                                    await asyncio.sleep(0.2)
                        except:
                            raise
        except:
            raise
    flag = 0
    while flag == 0 and stop == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            if msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '0':
                                flag = 1
                                stop = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=user.getid(),
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = continuetext
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid():
                                mes = msg['object']['message']['text']
                                mes = mes.split(' ')
                                if len(mes) != 2:
                                    res = await fetch(MSG_URL.format(
                                        user_id=user.getid(),
                                        random_id=random.randint(100000000,
                                                                 10000000000),
                                        message = wrongdatetimeformat
                                    ))
                                    print(res)
                                    await asyncio.sleep(0.2)
                                else:
                                    date = mes[0]
                                    date = date.split('-')
                                    if len(date) != 3:
                                        res = await fetch(MSG_URL.format(
                                            user_id=user.getid(),
                                            random_id=random.randint(100000000,
                                                                     10000000000),
                                            message = wrongdatetimeformat
                                        ))
                                        print(res)
                                        await asyncio.sleep(0.2)
                                    else:
                                        try:
                                            date[0] = int(date[0])
                                            date[1] = int(date[1])
                                            date[2] = int(date[2])
                                            days = [None, 31, None, 31, 30, 31,
                                                    30, 31, 31, 30, 31, 30, 31]
                                            if date[2] % 1000 == 0:
                                                days[2] = 29
                                            elif date[2] % 100 == 0:
                                                days[2] = 28
                                            elif date[2] % 4 == 0:
                                                days[2] = 29
                                            else:
                                                days[2] = 28
                                            if date[1] < 1 or date[1] > 12 or \
                                                    date[0] < 1 or date[0] > \
                                                    days[date[1]]:
                                                res = await fetch(MSG_URL.format
                                                    (
                                                    user_id=user.getid(),
                                                    random_id=random.randint\
                                                    (100000000, 10000000000),
                                                    message = wrongdaymonth
                                                ))
                                                print(res)
                                                await asyncio.sleep(0.2)
                                            else:
                                                times = mes[1]
                                                times = times.split('-')
                                                if len(times) != 2:
                                                    res = await fetch(MSG_URL.\
                                                        format(
                                                        user_id=user.getid(),
                                                        random_id=random.randint\
                                                            (100000000,
                                                             10000000000),
                                                        message = \
                                                            wrongdatetimeformat
                                                    ))
                                                    print(res)
                                                    await asyncio.sleep(0.2)
                                                else:
                                                    try:
                                                        times[0] = int(times[0])
                                                        times[1] = int(times[1])
                                                        if times[0] < 0 or times[0] > 23 or times[1] < 0 or times[0] > 59:
                                                            res = await fetch(MSG_URL.format(
                                                                user_id=user.getid(),
                                                                random_id=random.randint(100000000, 10000000000),
                                                                message = wrongtime
                                                                ))
                                                            print(res)
                                                            await asyncio.sleep(0.2)
                                                        else:
                                                            timezone = user.gettimezone()
                                                            #users = \
                                                            #    reloaduserdb()
                                                            #ind = users.index('#'+str(user.getid()))
                                                            #ind += 1
                                                            #timezone = int(users[ind])
                                                            curtime = time.mktime(time.localtime())
                                                            timeremind = time.mktime(time.struct_time((date[2], date[1], date[0], times[0], times[1], 0, 0, 0, 0))) + timecor[timezone]
                                                            if timeremind <= curtime:
                                                                res = await fetch(MSG_URL.format(
                                                                    user_id=user.getid(),
                                                                    random_id=random.randint(100000000, 10000000000),
                                                                    message = timeremindlessthancurtime
                                                                ))
                                                                print(res)
                                                                await asyncio.sleep(0.2)
                                                            else:
                                                                res = await fetch(MSG_URL.format(
                                                                    user_id=user.getid(),
                                                                    random_id=random.randint(100000000, 10000000000),
                                                                    message = addreminderenterfrequency
                                                                ))
                                                                print(res)
                                                                await asyncio.sleep(0.2)
                                                                flag = 1
                                                    except ValueError:
                                                        raise
                                        except ValueError:
                                            res = await fetch(MSG_URL.format(
                                                user_id=user.getid(),
                                                random_id=random.randint(100000000,
                                                                         10000000000),
                                                message = textnotnums
                                            ))
                                            print(res)
                                            await asyncio.sleep(0.2)
                        except:
                            raise
        except:
            raise
    flag = 0
    while flag == 0 and stop == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            mes = msg['object']['message']['text']
                            mes = mes.split(' ')
                            if msg['object']['message']['from_id'] == user.getid() and mes[0] == '0':
                                flag = 1
                                stop = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=user.getid(),
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = continuetext
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid() and mes[0] != '.' and len(mes) != 2:
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']['from_id'],
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = wrongfrequencyformat
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid():
                                if mes[0] == '.':
                                    repeattime = 0
                                    flag = 1
                                else:
                                    try:
                                        mes[0] = int(mes[0])
                                        if mes[1] != 'м' and mes[1] != 'ч' and \
                                                mes[1] != 'д' and mes[1] != 'н' and\
                                                mes[1] != 'мес' and mes[1] != 'г':
                                            res = await fetch(MSG_URL.format(
                                                user_id=user.getid(),
                                                random_id=random.randint(100000000,
                                                                        10000000000),
                                                message = wrongfrequencyvalue
                                            ))
                                            print(res)
                                            await asyncio.sleep(0.2)
                                        else:
                                            repeattime = mes[0]
                                            if mes[1] == 'м':
                                                repeattime *= 60
                                            elif mes[1] == 'ч':
                                                repeattime *= 3600
                                            elif mes[1] == 'д':
                                                repeattime *= 3600*24
                                            elif mes[1] == 'н':
                                                repeattime *= 3600*24*7
                                            elif mes[1] == 'мес':
                                                curtime = time.mktime((date[2],
                                                                    date[1],
                                                                    date[0],
                                                                    times[0],
                                                                    times[1],
                                                                    0, 0, 0, 0))
                                                curmonth = date[1]
                                                nextmonth = list((date[2], date[1],
                                                                date[0], times[0],
                                                                times[1], 0, 0, 0, 0))
                                                nextmonth[1] += int(mes[0])
                                                nextmonth[5] = 0
                                                nextmonth[6] = 0
                                                nextmonth[7] = 0
                                                nextmonth[8] = 0
                                                nextmonth = tuple(nextmonth)
                                                nextmonth = time.mktime(nextmonth)
                                                repeattime = nextmonth - curtime
                                            elif mes[1] == 'г':
                                                curtime = time.mktime((
                                                    date[2], date[1], date[0], times[0], times[1],
                                                    0, 0, 0, 0
                                                ))
                                                curmonth = date[1]
                                                nextmonth = list((date[2], date[1],
                                                                date[0], times[0],
                                                                times[1], 0, 0, 0, 0))
                                                nextmonth[0] += int(mes[0])
                                                nextmonth[5] = 0
                                                nextmonth[6] = 0
                                                nextmonth[7] = 0
                                                nextmonth[8] = 0
                                                nextmonth = tuple(nextmonth)
                                                nextmonth = time.mktime(nextmonth)
                                                repeattime = nextmonth - curtime
                                        flag = 1
                                    except ValueError:
                                        res = await fetch(MSG_URL.format(
                                        user_id=user.getid(),
                                        random_id=random.randint(100000000,
                                                                 10000000000),
                                        message = textnotnums
                                        ))
                                        print(res)
                                        await asyncio.sleep(0.2)
                                #flag = 1
                        except:
                            raise
        except:
            raise
    if stop == 0:
        user.addreminder(remindtext, timeremind, repeattime)
        # connection = engine.connect()
        # trans = connection.begin()
        # connection.execute("insert into `reminders` (`user`, `text`, `time`, `repeattime`) values ('"+str(user.getid())+"', '"+remindtext+"', '"+str(timeremind)+"', '"+str(repeattime)+"')")
        # trans.commit()
        # connection.close()
        # #ind = users.index('#'+str(msg['object']\
        # #                              ['message']\
        # #                              ['from_id']))
        # #ind += 2
        # #users.insert(ind, '~'+remindtext)
        # #ind += 1
        # #users.insert(ind, str(timeremind))
        # #ind += 1
        # #users.insert(ind, str(repeattime))
        # #def func(users):
        # #    fl = open('users.db', 'w')
        # #    fl.write('\n'.join(users))
        # #    fl.close()
        # #filequeue.append([func, users])
        # updatenotifications()
        res = await fetch(MSG_URL.format(
            user_id=user.getid(),
            
            random_id=random.randint(100000000,
                                        10000000000),
            message = reminderadded
        ))
        print(res)
    await asyncio.sleep(0.2)
    #flag = 1
                            
                            
                        
    await asyncio.sleep(1)
async def viewreminders(user, params):
    res = await fetch(MSG_URL.format(
        user_id=user.getid(),
        random_id=random.randint(100000000, 10000000000),
        message = reminderslist
    ))
    print(res)
    # connection = engine.connect()
    # data = connection.execute('select * from reminders where user='+str(user.getid()))
    # connection.close()
    # prelst = []
    # try:
    #     while True:
    #         prelst.append(data.next())
    # except StopIteration:
    #     pass
    prelst = user.getreminders(user)
    #users = reloaduserdb()
    #ind = users.index('#'+str(user.getid()))
    #ind += 2
    #lst = []
    #try:
    #    while users[ind][0] != '#':
    #        if users[ind][0] == '~':
    #            lst.append(users[ind][1:])
    #        ind += 1
    #except IndexError:
    #    pass
    ind2 = 1
    for i in prelst:
        res = await fetch(MSG_URL.format(
            user_id=user.getid(),
            random_id=random.randint(100000000, 10000000000),
            message = str(ind2)+'. '+i.gettext()
        ))
        print(res)
        ind2 += 1
        
        await asyncio.sleep(0.2)
    prelst.insert(0, None)
    flag = 0
    stop = 0
    while flag == 0 and stop == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            if msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '0':
                                flag = 1
                                stop = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=user.getid(),
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = continuetext
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid():
                                try:
                                    no = int(msg['object']['message']['text'])
                                    if no < 1 or no > len(prelst)-1:
                                        raise ValueError
                                    else:
                                        flag = 1
                                        res = await fetch(MSG_URL.format(
                                            user_id=user.getid(),
                                            random_id=random.randint(100000000,
                                                                     10000000000),
                                            message = editremindertext
                                        ))
                                        print(res)
                                        await asyncio.sleep(0.2)
                                except ValueError:
                                    res = await fetch(MSG_URL.format(
                                    user_id=user.getid(),
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = enterreminder
                                    ))
                                    print(res)
                                    await asyncio.sleep(0.2)
                        except:
                            raise
        except:
            raise
    flag = 0
    while flag == 0 and stop == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            if msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '0':
                                flag = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=user.getid(),
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = continuetext
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '1':
                                tasklist.append([msg['object']['message']['from_id'], asyncio.gather(editreminder(user, prelst.copy(), no, params.copy()))])
                                flag = 1
                            elif msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '2':
                                tasklist.append([msg['object']['message']['from_id'], asyncio.gather(delreminder(user, prelst.copy(), no, params.copy()))])
                                flag = 1
                            elif msg['object']['message']['from_id'] == user.getid():
                                tasklist.append([msg['object']['message']['from_id'], asyncio.gather(wronganswer(user))])
                        except:
                            raise
        except:
            raise
    await asyncio.sleep(1)
async def editreminder(user, lst, no, params):
    res = await fetch(MSG_URL.format(
        user_id=user.getid(),
        random_id=random.randint(100000000, 10000000000),
        message = editreminderentertext
    ))
    print(res)
    await asyncio.sleep(0.2)
    flag = 0
    stop = 0
    while flag == 0 and stop == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                    '9']
                            if msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '0':
                                flag = 1
                                stop = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']['from_id'],
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = continuetext
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '-':
                                remindtext = None
                                flag = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']['from_id'],
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = editreminderentertime
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid() and (msg['object']['message']['text'][0] in nums or\
                                    msg['object']['message']['text'][0] == '#'):
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']['from_id'],
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = editreminderwrongtext
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid():
                                remindtext = msg['object']['message']['text']
                                flag = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']['from_id'],
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = editreminderentertime
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                        except:
                            raise
        except:
            raise
    flag = 0
    while flag == 0 and stop == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            if msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '0':
                                flag = 1
                                stop = 1
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']['from_id'],
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = continuetext
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '-':
                                flag = 1
                                timeremind = None
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']['from_id'],
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = editreminderenterfrequency
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                            elif msg['object']['message']['from_id'] == user.getid():
                                mes = msg['object']['message']['text']
                                mes = mes.split(' ')
                                if len(mes) != 2:
                                    res = await fetch(MSG_URL.format(
                                        user_id=msg['object']['message']\
                                            ['from_id'],
                                        random_id=random.randint(100000000,
                                                                 10000000000),
                                        message = wrongdatetimeformat
                                    ))
                                    print(res)
                                    await asyncio.sleep(0.2)
                                else:
                                    date = mes[0]
                                    date = date.split('-')
                                    if len(date) != 3:
                                        res = await fetch(MSG_URL.format(
                                            user_id=msg['object']['message']\
                                                ['from_id'],
                                            random_id=random.randint(100000000,
                                                                     10000000000),
                                            message = wrongdatetimeformat
                                        ))
                                        print(res)
                                        await asyncio.sleep(0.2)
                                    else:
                                        date[0] = int(date[0])
                                        date[1] = int(date[1])
                                        date[2] = int(date[2])
                                        days = [None, 31, None, 31, 30, 31, 30,
                                                31, 31, 30, 31, 30, 31]
                                        if date[2] % 1000 == 0:
                                            days[2] = 29
                                        elif date[2] % 100 == 0:
                                            days[2] = 28
                                        elif date[2] % 4 == 0:
                                            days[2] = 29
                                        else:
                                            days[2] = 28
                                        if date[1] > 12 or date[1] < 1 or \
                                                date[0] < 1 or date[0] >\
                                                days[date[1]]:
                                            res = await fetch(MSG_URL.format(
                                                user_id=msg['object']['message']\
                                                    ['from_id'],
                                                random_id=random.randint(100000000,
                                                                         10000000000),
                                                message = wrongdaymonth
                                            ))
                                            print(res)
                                            await asyncio.sleep(0.2)
                                        else:
                                            times = mes[1]
                                            times = times.split('-')
                                            times[0] = int(times[0])
                                            times[1] = int(times[1])
                                            if len(times) != 2:
                                                res = await fetch(MSG_URL.format(
                                                    user_id=msg['object']['message']\
                                                        ['from_id'],
                                                    random_id=random.randint\
                                                    (100000000, 10000000000),
                                                    message = wrongdatetimeformat
                                                ))
                                                print(res)
                                                await asyncio.sleep(0.2)
                                            elif times[0] < 0 or times[0] > 23 \
                                                    or times[1] < 0 or times[1]\
                                                    > 59:
                                                res = await fetch(MSG_URL.format(
                                                    user_id=msg['object']['message']\
                                                        ['from_id'],
                                                    random_id=random.randint\
                                                        (100000000, 10000000000),
                                                    message = wrongtime
                                                ))
                                                print(res)
                                                await asyncio.sleep(0.2)
                                            else:
                                                timezone = user.gettimezone()
                                                # connection = engine.connect()
                                                # data = connection.execute('select * from users where user='+str(msg\
                                                # ['object']['message']['from_id']))
                                                # connection.close()
                                                # userdata = data.next()
                                                # timezone = userdata[2]
                                                # #users = reloaduserdb()
                                                # #ind = users.index('#'+str(msg\
                                                # #['object']['message']['from_id']))
                                                # #ind += 1
                                                # #timezone = int(users[ind])
                                                curtime = time.mktime(time.localtime())
                                                timeremind = time.mktime(time.\
                                                    struct_time((date[2], date[1],
                                                                 date[0], times[0],
                                                                 times[1], 0, 0,
                                                                 0, 0)))+timecor[timezone]
                                                if timeremind <= curtime:
                                                    res = await fetch(MSG_URL.\
                                                        format(
                                                        user_id=msg['object']\
                                                            ['message']['from_id'],
                                                        random_id=random.randint\
                                                            (100000000, 10000000000),
                                                        message = timeremindlessthancurtime
                                                    ))
                                                    print(res)
                                                    await asyncio.sleep(0.2)
                                                else:
                                                    flag = 1
                                                    res = await fetch(MSG_URL.\
                                                        format(
                                                        user_id=msg['object']\
                                                            ['message']['from_id'],
                                                        random_id=random.randint\
                                                            (100000000, 10000000000),
                                                        message = editreminderenterfrequency
                                                    ))
                                                    print(res)
                                                    await asyncio.sleep(0.2)
                        except:
                            raise
        except:
            raise
    flag = 0
    while flag == 0 and stop == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            if msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '0':
                                flag = 1
                                stop = 1
                            elif msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '-':
                                repeattime = None
                                flag = 1
                            elif msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '.':
                                repeattime = 0
                                flag = 1
                            if msg['object']['message']['from_id'] == user.getid() and flag == 0:
                                flag = 1
                                mes = msg['object']['message']['text'].split(' ')
                                if mes[0] == '-':
                                    mes.append('')
                                elif mes[1] != 'м' and mes[1] != 'ч' and mes[1]\
                                        != 'д' and mes[1] != 'н' and mes[1] !=\
                                        'мес' and mes[1] != 'г':
                                    res = await fetch(MSG_URL.format(
                                        user_id=msg['object']['message']\
                                            ['from_id'],
                                        random_id=random.randint(100000000,
                                                                 10000000000),
                                        message = wrongfrequencyvalue
                                    ))
                                    print(res)
                                    flag = 0
                                    await asyncio.sleep(0.2)
                                elif mes[1] == 'м':
                                    repeattime = 60*int(mes[0])
                                elif mes[1] == 'ч':
                                    repeattime = 3600*int(mes[0])
                                elif mes[1] == 'д':
                                    repeattime = 3600*24*int(mes[0])
                                elif mes[1] == 'н':
                                    repeattime = 3600*24*7*int(mes[0])
                                elif mes[1] == 'мес':
                                    curtime = time.mktime((date[2], date[1],
                                                           date[0], times[0],
                                                           times[1], 0, 0, 0, 0))
                                    curmonth = date[1]
                                    nextmonth = list((date[2], date[1], date[0],
                                                      times[0], times[1], 0, 0, 0, 0))
                                    nextmonth[1] += int(mes[0])
                                    nextmonth[5] = 0
                                    nextmonth[6] = 0
                                    nextmonth[7] = 0
                                    nextmonth[8] = 0
                                    nextmonth = tuple(nextmonth)
                                    nextmonth = time.mktime(nextmonth)
                                    repeattime = nextmonth - curtime
                                elif mes[1] == 'г':
                                    curtime = time.mktime((date[2], date[1],
                                                           date[0], times[0],
                                                           times[1], 0, 0, 0, 0))
                                    curmonth = date[1]
                                    nextmonth = list((date[2], date[1], date[0],
                                                      times[0], times[1], 0, 0, 0, 0))
                                    nextmonth[0] += int(mes[0])
                                    nextmonth[5] = 0
                                    nextmonth[6] = 0
                                    nextmonth[7] = 0
                                    nextmonth[8] = 0
                                    nextmonth = tuple(nextmonth)
                                    nextmonth = time.mktime(nextmonth)
                                    repeattime = nextmonth - curtime
                            if flag == 1:
                                remindid = lst[no].getid()
                                user.editreminder(remindid, remindtext, timeremind, repeattime)
                                # connection = engine.connect()
                                # trans = connection.begin()
                                # #users = reloaduserdb()
                                # #ind = users.index('~'+lst[no])
                                # if remindtext:
                                #     connection.execute("update reminders set text = '"+remindtext+"' where reminders.id = "+str(remindid))
                                # #ind += 1
                                # if timeremind:
                                #     connection.execute("update reminders set time = '"+str(timeremind)+"' where reminders.id = "+str(remindid))
                                # #ind += 1
                                # if repeattime:
                                #     connection.execute("update reminders set repeattime = '"+str(repeattime)+"' where reminders.id = "+str(remindid))
                                # trans.commit()
                                # connection.close()
                                #def func(users):
                                #    fl = open('users.db', 'w')
                                #    fl.write('\n'.join(users))
                                #    fl.close()
                                #filequeue.append([func, users])
                                
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']\
                                        ['from_id'],
                                    random_id=random.randint(100000000,
                                                                10000000000),
                                    message = reminderedited
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                        except:
                            raise
        except:
            raise        
    await asyncio.sleep(1)
async def delreminder(user, lst, no, params):
    res = await fetch(MSG_URL.format(
        user_id=user.getid(),
        random_id=random.randint(100000000, 10000000000),
        message = areyousure
    ))
    print(res)
    await asyncio.sleep(0.2)
    flag = 0
    stop = 0
    while flag == 0 and stop == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            if msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '0':
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']['from_id'],
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = continuetext
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                                flag = 1
                            elif msg['object']['message']['from_id'] == user.getid() and msg['object']['message']['text'] == '1':
                                ind = lst[no][0]
                                user.delreminder(ind)
                                # connection = engine.connect()
                                # trans = connection.begin()
                                # connection.execute('delete from reminders where reminders.id = '+str(ind))
                                # trans.commit()
                                # connection.close()
                                # #users = reloaduserdb()
                                # #ind = users.index('~'+lst[no])
                                # #del users[ind]
                                # #del users[ind]
                                # #del users[ind]
                                # #def func(users):
                                # #    fl = open('users.db', 'w')
                                # #    fl.write("\n".join(users))
                                # #    fl.close()
                                # #filequeue.append([func, users])
                                # updatenotifications()
                                res = await fetch(MSG_URL.format(
                                    user_id=msg['object']['message']['from_id'],
                                    random_id=random.randint(100000000,
                                                             10000000000),
                                    message = reminderdeleted
                                ))
                                print(res)
                                await asyncio.sleep(0.2)
                                flag = 1
                            elif msg['object']['message']['from_id'] == user.getid():
                                await wronganswer(user)
                        except:
                            raise
        except:
            raise
    await asyncio.sleep(1)
async def register(user, params):
    message=registertime
    message = message.split('\n')
    for i in message:
        res = await fetch(MSG_URL.format(
            user_id=user.getid(),
            random_id=random.randint(100000000, 10000000000),
            message = i
            ))
        print(res)
        await asyncio.sleep(0.2)
    flag = 0
    while flag == 0:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = json.loads(await fetch(long_pool_url))
            
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        try:
                            if user.getid() == msg['object']['message']['from_id'] and 1 <= int(msg['object']['message']['text']) <= 36 :
                                tasklist.append([msg['object']['message']['from_id'], asyncio.gather(end_register(user, int(msg['object']['message']['text'])))])
                                flag = 1
                            elif user.getid() != msg['object']['message']['from_id']:
                                pass
                            else:
                                raise ValueError
                        except ValueError:
                            tasklist.append([user.getid(), asyncio.gather(wronganswer(user))])
        except:
            raise
    await asyncio.sleep(1)
async def end_register(user, tz):
    user.write(tz)
    # connection = engine.connect()
    # trans = connection.begin()
    # connection.execute('insert into users(user, timezone) values ('+str(user.getid())+', '+str(tz))
    # trans.commit()
    # connection.close()
    #def func(writing):
    #    fl = open('users.db', 'a')
    #    fl.write(writing)
    #    fl.close()
    #filequeue.append([func, '#'+str(msg['object']['message']['from_id'])+'\n'+msg['object']\
    #        ['message']['text']+'\n'])
    #users = reloaduserdb()
    res = await fetch(MSG_URL.format(
        user_id=user.getid(),
        random_id=random.randint(100000000, 10000000000),
        message=userregistered
    ))
    print(res)
    await asyncio.sleep(1)
def reloaduserdb():
    fl = open('users.db')
    users = fl.read()
    users = users.split('\n')
    fl.close()
    return users
async def wronganswer(user):
    res = await fetch(MSG_URL.format(
        user_id=user.getid(),
        random_id=random.randint(100000000, 10000000000),
        message=wronganswertext
    ))
    print(res)
    await asyncio.sleep(1)
async def pong(user):
    res = await fetch(MSG_URL.format(
        user_id=user,
        random_id=random.randint(100000000, 10000000000),
        message=pongtext
    ))
    print(res)
    await asyncio.sleep(1)


async def begin(user2, msgtext, params):
    #users = reloaduserdb()
    connection = engine.connect()
    userdata = connection.execute('select * from users where user='+str(user2.getid()))
    connection.close()
    user = []
    try:
        while True:
            user.append(userdata.next())
    except StopIteration:
        pass
    for i in range(0, len(user)):
        user[i] = user[i][1]
    if not user2.getid() in user and msgtext != 'Начать':
        res = await fetch(MSG_URL.format(
            user_id=user2.getid(),
            random_id=random.randint(100000000, 10000000000),
            message=welcome
        ))
        print(res)
    elif not user2.getid() in user and msgtext == 'Начать':
        tasklist.append([user2.getid(), asyncio.gather(register(user2, params.copy()))])
        #successreg = 0
        #while successreg == 0:
        #    try:
        #        if not '#'+str(msg['object']['message']['from_id']) in users \
        #        and msg['object']['message']['text'] != 'Начать' and 1 <= int\
        #        (msg['object']['message']['text']) <= 36:
        #            await end_register()
        #            successreg = 1
        #        #elif msg['object']['message']['text'] == 'Начать':
        #        #    pass
        #    except ValueError:
        #        await wronganswer()
    else:
        tasklist.append([user2.getid(), asyncio.gather(mainwindow(user2, params.copy()))])
    await asyncio.sleep(1)
