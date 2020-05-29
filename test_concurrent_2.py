import concurrent
from concurrent.futures.thread import ThreadPoolExecutor
import time
import threading


def call_script(thread_id, arg, heartbeat, die):
    print('Thread', thread_id, 'argument:', arg)
    while True:
        if die.is_set():
            break
        if arg == "argumentsB":
            time.sleep(1)
            raise Exception
        else:
            time.sleep(4)
        heartbeat.set()
        print('Thread', thread_id, 'Finished')


thread_parameters = []
args = ['argumentsA', 'argumentsB', 'argumentsC']
for i in range(len(args)):
    thread_parameters.append({
        'heartbeat': threading.Event(),
        'terminate': threading.Event(),
        'id': i,
        'arg': args[i]
    })

with ThreadPoolExecutor(max_workers=5) as executor:
    ordinal = 1
    fs = []
    for i in range(len(thread_parameters)):
        f = executor.submit(
            call_script,
            thread_parameters[i]['id'],
            thread_parameters[i]['arg'],
            thread_parameters[i]['heartbeat'],
            thread_parameters[i]['terminate']
        )
        # fs.append(f)
        ordinal += 1

    while True:
        for i in range(len(thread_parameters)):
            h = thread_parameters[i]['heartbeat'].wait(timeout=2)
            if not h:
                print("timeout expired for thread: {}".format(i))
                thread_parameters[i]['terminate'].set()
                print("spinning new thread: {}".format(i))
                f = executor.submit(
                    call_script,
                    thread_parameters[i]['id'],
                    thread_parameters[i]['arg'],
                    thread_parameters[i]['heartbeat'],
                    thread_parameters[i]['terminate']
                )
            thread_parameters[i]['heartbeat'].clear()

    # done, not_done = concurrent.futures.wait(fs, return_when=concurrent.futures.FIRST_EXCEPTION)
    # for f in done:
    #     print("done: {}".format(f.ordinal))
    # for f in not_done:
    #     print("not done: {}".format(f.ordinal))
print('All tasks has been finished')
