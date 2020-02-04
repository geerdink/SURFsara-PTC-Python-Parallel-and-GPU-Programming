import threading
import time

def daemon():
    print('Starting daemon')
    time.sleep(2)
    print('Exiting daemon')

def non_daemon():
    print('Starting NON daemon')
    print('Exiting NON daemon')

d = threading.Thread(name='daemon', target=daemon, daemon=True)
t = threading.Thread(name='non-daemon', target=non_daemon, daemon=False)

d.start()
t.start()
# if you don't join the threads, the daemon thread will not complete.
