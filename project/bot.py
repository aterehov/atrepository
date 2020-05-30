from handlers import *


async def main():
    global tasklist
    global openusers
    updatenotifications()
    #notificatorthread = Thread(target=notifier)
    #notificatorthread.start()
    res = await fetch(URL)
    res = json.loads(res)
    params = res['response']
    tasklist.append(['NotifyService', asyncio.create_task(notifier())])
    tasklist.append(['System', asyncio.create_task(taskmanager())])
    #tasklist.append(['FileSystem', asyncio.create_task(filewriter())])
    while True:
        long_pool_url = LONG_POOL_URL.format(**params)
        try:
            res = await fetch(long_pool_url)
            res = json.loads(res)
            if res and res['updates']:
                params['ts'] = res['ts']
                for msg in res['updates']:
                    if 'text' not in msg['object']:
                        print('Process msg')
                        if msg['object']['message']['text'] == 'ping':
                            tasklist.append(asyncio.gather(pong(msg.copy())))
                        else:
                            if msg['object']['message']['from_id'] not in openusers:
                                newuser = user(msg['object']['message']['from_id'])
                                #newuser.id = msg['object']['message']['from_id']
                                openusers.append(msg['object']['message']['from_id'])
                                #users.append(newuser)
                                tasklist.append([msg['object']['message']['from_id'], asyncio.create_task(begin(newuser, msg['object']['message']['text'], params.copy()))])
                            else:
                                pass
        except:
            await asyncio.sleep(15)
            raise
        else:
            print('reconnect')
            await asyncio.sleep(1)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('\nPlease wait...')
