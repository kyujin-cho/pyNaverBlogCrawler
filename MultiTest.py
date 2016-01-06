import urllib
from multiprocessing import Process, Queue
import os
import time
def dl(url ,q):
    print("DLing {:s}...".format(url))
    q.put(urllib.request.urlopen(url).read)

def f(name):
    print('%s\'s pid : %d' %(name, os.getpid()))

if __name__ == '__main' :
    q = Queue()
    p1 = Process(target=f, args=("haru",))
    p2 = Process(target=f, args=("chiha",))

    p1.start()
    p2.start()
    time.sleep(2)
    p1.join()
    p2.join()




