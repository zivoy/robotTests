import threading
from time import sleep

def worker():
    """thread worker function"""
    print 'Worker start' 
    sleep(9)
    print 'done'
    return



def worker2():
    """thread worker function"""
    print 'Worker start 222' 
    sleep(10)
    print 'done 222'
    return



threads = []
t = threading.Thread(target=worker2)
t.start()
for i in range(5):
    sleep(2)
    t = threading.Thread(target=worker)
    threads.append(t)
    print i,threads
    t.start()

