"""Модуль с обработчиками сообщений"""
from string import digits as nums

from utils import *



async def main_window(user):
    """Открывает главное меню и исполняет желание пользователя"""
    write_list.append((user._id, MAIN_WINDOW_TEXT))
    
    flag = 0
    while flag == 0:
        if len(read_list[user._id]) > 0:          
            if read_list[user._id][0] == '1':
                task_list.append([user._id, 
                                asyncio.gather(change_time(user))])
                flag = 1
            elif read_list[user._id][0] == '2':
                task_list.append([user._id, 
                                asyncio.gather(add_reminder(user))])
                flag = 1
            elif read_list[user._id][0] == '3':
                task_list.append([user._id, 
                                asyncio.gather(view_reminders(user))])
                flag = 1
            else:
                await wrong_answer(user)
            del read_list[user._id][0]        
        await asyncio.sleep(TIMEOUT)


async def change_time(user):
    """Узнает, в каком часовом поясе находится пользователь, и изменяет его"""
    message=CHANGE_TIME_TEXT.split('\n')
    for i in message:
        write_list.append((user._id, i))
    flag = 0
    while flag == 0:
        if len(read_list[user._id]) > 0:
            try:
                if 1 <= int(read_list[user._id][0]) <= 36:
                    await user.change_timezone(int(read_list[user._id][0]))
                    flag = 1
                    write_list.append((user._id, EDIT_TIME_TEXT))
                elif int(read_list[user._id][0]) == 0:
                    flag = 1
                    write_list.append((user._id, CONTINUE_TEXT))
                else:
                    await wrong_answer(user)
            except ValueError:
                await wrong_answer(user)
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)
    await asyncio.sleep(TIMEOUT)


async def add_reminder(user):
    """Помогает пользователю добавить напоминание"""
    write_list.append((user._id, ADD_REMINDER_ENTER_TEXT))
    flag = 0
    stop = 0
    while flag == 0:
        if len(read_list[user._id]) > 0:
            if read_list[user._id][0] == '0':
                flag = 1
                write_list.append((user._id, CONTINUE_TEXT))
                stop = 1
            else:
                if "'" in read_list[user._id][0] or '"' in read_list[user._id][0] or ';' in read_list[user._id][0]:
                    write_list.append((user._id, ADD_REMINDER_WRONG_TEXT))
                else:
                    remindtext = read_list[user._id][0]
                    flag = 1
                    write_list.append((user._id, ADD_REMINDER_ENTER_TIME))
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)
    flag = 0
    while flag == 0 and stop == 0:
        if len(read_list[user._id]) > 0:
            if read_list[user._id][0] == '0':
                flag = 1
                stop = 1
                write_list.append((user._id, CONTINUE_TEXT))
            else:
                mes = read_list[user._id][0].split(' ')
                if len(mes) != 2:
                    write_list.append((user._id, WRONG_DATE_TIME_FORMAT))
                else:
                    date = mes[0].split('-')
                    if len(date) != 3:
                        write_list.append((user._id, WRONG_DATE_TIME_FORMAT))
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
                                write_list.append((user._id, WRONG_DAY_MONTH))
                            else:
                                times = mes[1].split('-')
                                if len(times) != 2:
                                    write_list.append((user._id, 
                                                        WRONG_DATE_TIME_FORMAT))
                                else:
                                    try:
                                        times[0] = int(times[0])
                                        times[1] = int(times[1])
                                        if times[0] < 0 or times[0] > 23 or times[1] < 0 or times[0] > 59:
                                            write_list.append((user._id, 
                                                                WRONG_TIME))
                                        else:
                                            timezone = await user.get_timezone()
                                            curtime = timegm(time.gmtime())
                                            timeremind = timegm(
                                                    time.struct_time((date[2], 
                                                                    date[1], 
                                                                    date[0], 
                                                                    times[0], 
                                                                    times[1], 
                                                                    0, 0, 0, 0))
                                                    ) + TIME_COR[timezone]
                                            if timeremind <= curtime:
                                                write_list.append((user._id, 
                                                    TIMEREMIND_LESS_THAN_CURTIME))
                                            else:
                                                write_list.append((user._id, 
                                                    ADD_REMINDER_ENTER_FREQUENCY))
                                                flag = 1
                                    except ValueError:
                                        raise
                        except ValueError:
                            write_list.append((user._id, TEXT_NOT_NUMS))
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)
        
    flag = 0
    while flag == 0 and stop == 0:
        if len(read_list[user._id]) > 0:
            mes = read_list[user._id][0].split(' ')
            if mes[0] == '0':
                flag = 1
                stop = 1
                write_list.append((user._id, CONTINUE_TEXT))
            elif mes[0] != '.' and len(mes) != 2:
                write_list.append((user._id, WRONG_FREQUENCY_FORMAT))
            else:
                if mes[0] == '.':
                    repeattime = 0
                    flag = 1
                else:
                    try:
                        mes[0] = int(mes[0])
                        if mes[1] != 'м' and mes[1] != 'ч' and \
                                mes[1] != 'д' and mes[1] != 'н' and\
                                mes[1] != 'мес' and mes[1] != 'г':
                            write_list.append((user._id, 
                                                WRONG_FREQUENCY_VALUE))
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
                                curtime = timegm((date[2],
                                                    date[1],
                                                    date[0],
                                                    times[0],
                                                    times[1],
                                                    0, 0, 0, 0))
                                nextmonth = timegm((date[2], date[1] + int(mes[0]),
                                                date[0], times[0],
                                                times[1], 0, 0, 0, 0))
                                repeattime = nextmonth - curtime
                            elif mes[1] == 'г':
                                curtime = timegm((date[2], date[1], date[0], 
                                            times[0], times[1], 0, 0, 0, 0))
                                nextmonth = timegm((date[2] + int(mes[0]), date[1], date[0], 
                                            times[0], times[1], 0, 0, 0, 0))
                                repeattime = nextmonth - curtime
                        flag = 1
                    except ValueError:
                        write_list.append((user._id, TEXT_NOT_NUMS))
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)
    if flag == 1:
        await user.add_reminder(remindtext, timeremind, repeattime)
        write_list.append((user._id, REMINDER_ADDED))
    await asyncio.sleep(TIMEOUT)


async def view_reminders(user):
    """Показывает напоминания пользовтеля и спрашивает, что он хочет с ними сделать"""
    write_list.append((user._id, REMINDERS_LIST))
    prelst = await user.get_reminders()
    ind2 = 1
    for i in prelst:
        write_list.append((user._id, str(ind2)+'. '+i._text))
        ind2 += 1
        
    
    prelst.insert(0, None)
    flag = 0
    stop = 0
    while flag == 0 and stop == 0:
        if len(read_list[user._id]) > 0:
            if read_list[user._id][0] == '0':
                flag = 1
                stop = 1
                write_list.append((user._id, CONTINUE_TEXT))
            else:
                try:
                    no = int(read_list[user._id][0])
                    if no < 1 or no > len(prelst)-1:
                        raise ValueError
                    else:
                        flag = 1
                        write_list.append((user._id, EDIT_REMINDER_TEXT))
                except ValueError:
                    write_list.append((user._id, ENTER_REMINDER))
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)
    flag = 0
    while flag == 0 and stop == 0:
        if len(read_list[user._id]) > 0:
            if read_list[user._id][0] == '0':
                flag = 1
                write_list.append((user._id, CONTINUE_TEXT))
            elif read_list[user._id][0] == '1':
                task_list.append([user._id, asyncio.gather(edit_reminder(user,
                                                        prelst.copy(), no))])
                flag = 1
            elif read_list[user._id][0] == '2':
                task_list.append([user._id, asyncio.gather(del_reminder(user, 
                                                        prelst.copy(), no))])
                flag = 1
            else:
                task_list.append([user._id, asyncio.gather(wrong_answer(user))])
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)


async def edit_reminder(user, lst, no):
    """Помогает пользователю изменить напоминание"""
    write_list.append((user._id, EDIT_REMINDER_ENTER_TEXT))
    flag = 0
    stop = 0
    while flag == 0 and stop == 0:
        if len(read_list[user._id]) > 0:
            if read_list[user._id][0] == '0':
                flag = 1
                stop = 1
                write_list.append((user._id, CONTINUE_TEXT))
            elif read_list[user._id][0] == '-':
                remindtext = None
                flag = 1
                write_list.append((user._id, EDIT_REMINDER_ENTER_TIME))
            elif "'" in read_list[user._id][0] or '"' in read_list[user._id][0] or ';' in read_list[user._id][0]:
                write_list.append((user._id, EDIT_REMINDER_WRONG_TEXT))
            else:
                remindtext = read_list[user._id][0]
                flag = 1
                write_list.append((user._id, EDIT_REMINDER_ENTER_TIME))
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)
    flag = 0
    while flag == 0 and stop == 0:
        if len(read_list[user._id]) > 0:
            if read_list[user._id][0] == '0':
                flag = 1
                stop = 1
                write_list.append((user._id, CONTINUE_TEXT))
            elif read_list[user._id][0] == '-':
                flag = 1
                timeremind = None
                write_list.append((user._id, EDIT_REMINDER_ENTER_FREQUENCY))
            else:
                mes = read_list[user._id][0]
                mes = mes.split(' ')
                if len(mes) != 2:
                    write_list.append((user._id, WRONG_DATE_TIME_FORMAT))
                else:
                    date = mes[0].split('-')
                    if len(date) != 3:
                        write_list.append((user._id, WRONG_DATE_TIME_FORMAT))
                    else:
                        try:
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
                                write_list.append((user._id, WRONG_DAY_MONTH))
                            else:
                                try:
                                    times = mes[1].split('-')
                                    times[0] = int(times[0])
                                    times[1] = int(times[1])
                                    if len(times) != 2:
                                        write_list.append((user._id, 
                                                WRONG_DATE_TIME_FORMAT))
                                    elif times[0] < 0 or times[0] > 23 \
                                            or times[1] < 0 or times[1]\
                                            > 59:
                                        write_list.append((user._id, 
                                                            WRONG_TIME))
                                    else:
                                        timezone = await user.get_timezone()
                                        curtime = timegm(time.gmtime())
                                        timeremind = timegm(time.struct_time((
                                                date[2], date[1], date[0], 
                                                times[0], times[1], 0, 0, 0, 0)
                                                ))+TIME_COR[timezone]
                                        if timeremind <= curtime:
                                            write_list.append((user._id, 
                                                TIMEREMIND_LESS_THAN_CURTIME))
                                        else:
                                            flag = 1
                                            write_list.append((user._id, 
                                                EDIT_REMINDER_ENTER_FREQUENCY))
                                except IndexError:
                                    write_list.append((user._id, 
                                                        WRONG_DATE_TIME_FORMAT))
                        except ValueError:
                            write_list.append((user._id, TEXT_NOT_NUMS))
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)
    flag = 0
    while flag == 0 and stop == 0:
        if len(read_list[user._id]) > 0:
            if read_list[user._id][0] == '0':
                flag = 1
                stop = 1
            elif read_list[user._id][0] == '-':
                repeattime = None
                flag = 1
            elif read_list[user._id][0] == '.':
                repeattime = 0
                flag = 1
            else:
                try:
                    mes = read_list[user._id][0].split(' ')
                    if mes[0] == '-':
                        mes.append('')
                        flag = 1
                    elif int(mes[0]) <= 0:
                        write_list.append((user._id, WRONG_REPEATTIME_VALUE))
                    elif mes[1] != 'м' and mes[1] != 'ч' and mes[1]\
                            != 'д' and mes[1] != 'н' and mes[1] !=\
                            'мес' and mes[1] != 'г':
                        write_list.append((user._id, WRONG_FREQUENCY_VALUE))
                    elif mes[1] == 'м':
                        repeattime = 60*int(mes[0])
                        flag = 1
                    elif mes[1] == 'ч':
                        repeattime = 3600*int(mes[0])
                        flag = 1
                    elif mes[1] == 'д':
                        repeattime = 3600*24*int(mes[0])
                        flag = 1
                    elif mes[1] == 'н':
                        repeattime = 3600*24*7*int(mes[0])
                        flag = 1
                    elif mes[1] == 'мес':
                        if timeremind is None:
                            a = time.gmtime(lst[no]._time)
                            date = (a.tm_mday, a.tm_mon, a.tm_year)
                            times = (a.tm_hour, a.tm_min)
                        curtime = timegm((date[2], date[1],
                                            date[0], times[0],
                                            times[1], 0, 0, 0, 0))
                        nextmonth = timegm((date[2], date[1] + int(mes[0]), date[0],
                                        times[0], times[1], 0, 0, 0, 0))
                        repeattime = nextmonth - curtime
                        flag = 1
                    elif mes[1] == 'г':
                        if timeremind is None:
                            a = time.gmtime(lst[no]._time)
                            date = (a.tm_mday, a.tm_mon, a.tm_year)
                            times = (a.tm_hour, a.tm_min)
                        curtime = timegm((date[2], date[1],
                                            date[0], times[0],
                                            times[1], 0, 0, 0, 0))
                        nextmonth = timegm((date[2] + int(mes[0]), date[1], date[0],
                                        times[0], times[1], 0, 0, 0, 0))
                        repeattime = nextmonth - curtime
                        flag = 1
                except IndexError:
                    write_list.append((user._id, WRONG_FREQUENCY_FORMAT))
            if flag == 1:
                remindid = lst[no]._id
                await user.edit_reminder(remindid, remindtext, timeremind, repeattime)
                write_list.append((user._id, REMINDER_EDITED))
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)
    await asyncio.sleep(TIMEOUT)


async def del_reminder(user, lst, no):
    """Помогает пользователю удалить напоминание"""
    write_list.append((user._id, ARE_YOU_SURE))
    flag = 0
    stop = 0
    while flag == 0 and stop == 0:
        if len(read_list[user._id]) > 0:
            if read_list[user._id][0] == '0':
                write_list.append((user._id, CONTINUE_TEXT))
                flag = 1
            elif read_list[user._id][0] == '1':
                ind = lst[no]._id
                await user.del_reminder(ind)
                write_list.append((user._id, REMINDER_DELETED))
                flag = 1
            else:
                await wrong_answer(user)
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)
    await asyncio.sleep(TIMEOUT)


async def register(user):
    """Помогает пользователю зарегистрироваться"""
    message=REGISTER_TIME.split('\n')
    for i in message:
        write_list.append((user._id, i))
    flag = 0
    while flag == 0:
        if len(read_list[user._id]) > 0:
            if 1 <= int(read_list[user._id][0]) <= 36 :
                await end_register(user, int(read_list[user._id][0]))
                flag = 1
            else:
                await wrong_answer(user)
            del read_list[user._id][0]
        await asyncio.sleep(TIMEOUT)
    await asyncio.sleep(TIMEOUT)


async def end_register(user, tz):
    """Завершает регистрацию пользователя"""
    await user.write(tz)
    write_list.append((user._id, USER_REGISTERED))
    await asyncio.sleep(TIMEOUT)


async def wrong_answer(user):
    """Сообщает пользователю, что он выбрал несуществующий вариант ответа"""
    write_list.append((user._id, WRONG_ANSWER_TEXT))
    await asyncio.sleep(TIMEOUT)

async def begin(user2, msgtext):
    """Определяет, что нужно сделать, в зависимости от того, зарегистрирован ли пользователь"""
    try:
        user = await read_db('select * from users where user=(%s)',
                                       (str(user2._id)))
    except Exception:
        write_list.append((user2._id, DB_ERROR_USER))
        raise
    try:
        if user2._id == user[0]['user']:
            task_list.append([user2._id, asyncio.gather(main_window(user2))])
    except IndexError:
        if msgtext.lower() != 'начать':
            write_list.append((user2._id, WELCOME))
        else:
            task_list.append([user2._id, asyncio.gather(register(user2))])        
    await asyncio.sleep(TIMEOUT)