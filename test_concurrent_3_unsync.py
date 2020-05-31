import concurrent
import time
import threading
import asyncio
from unsync import unsync

@unsync
async def takes_time(t):
    await asyncio.sleep(t)


@unsync
async def call_script(thread_id, arg):
    print('Thread', thread_id, 'argument:', arg)
    if arg == "argumentsB":
        await takes_time(1)
        # raise Exception
    else:
        await takes_time(4)
    print('Thread', thread_id, 'Finished')

@unsync(cpu_bound=True)
def very_compute_intensive():
    a = []
    a.append(1)
    a.append(1)
    for i in range(2,10):
        a.append(a[i-1] + a[i-2])
    return a


async def start(loop, thread_parameters):
    tasks = []
    for i in range(3):
        tasks.append(call_script(thread_parameters[i]['id'],thread_parameters[i]['arg']))
    tasks.append(very_compute_intensive())
    for task in tasks:
        result = task.result()
        print(result)

def main():
    thread_parameters = []
    args = ['argumentsA', 'argumentsB', 'argumentsC']
    for i in range(len(args)):
        thread_parameters.append({
            'id': i,
            'arg': args[i]
        })

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(loop, thread_parameters))
    loop.close()

    print('All tasks has been finished')

if __name__ == "__main__":
    main()

