import concurrent
from concurrent.futures.thread import ThreadPoolExecutor
import time
import threading


def call_script(thread_id, arg):
    print('Thread', thread_id, 'argument:', arg)
    if arg == "argumentsB":
        time.sleep(1)
        raise Exception
    else:
        time.sleep(4)
    print('Thread', thread_id, 'Finished')


thread_parameters = []
args = ['argumentsA', 'argumentsB', 'argumentsC']
for i in range(len(args)):
    thread_parameters.append({
        #'heartbeat': threading.Event(),
        #'terminate': threading.Event(),
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
            thread_parameters[i]['arg']
        )
        fs.append(f)
        ordinal += 1

    done, not_done = concurrent.futures.wait(fs, timeout=2, return_when=concurrent.futures.ALL_COMPLETED)
    for f in done:
        print("done within timeout: {}".format(f))
    for f in not_done:
        print("not done within timeout: {}".format(f))
print('All tasks has been finished')

