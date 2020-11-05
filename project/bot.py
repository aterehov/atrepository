from handlers import *


async def main():
    """Главная функция

    Запускает бота и обработку первых сообщений пользователей

    """
    await open_db_conn()
    await update_notifications()
    await login()
    task_list.append(('NotifyService', asyncio.create_task(notifier())))
    task_list.append(('System', asyncio.create_task(task_manager())))
    task_list.append(('WriteVK', asyncio.create_task(fetch_write())))
    task_list.append(('ReadVK', asyncio.create_task(fetch_read())))
    while True:
        for i in read_list:
            if len(read_list[i]) > 0 and i not in open_users:
                newuser = User(i)
                open_users.append(i)
                task_list.append((i, asyncio.create_task(begin(newuser, 
                                                            read_list[i][0]))))
                del read_list[i][0]
        await asyncio.sleep(TIMEOUT)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Ctrl-C - Stopped')