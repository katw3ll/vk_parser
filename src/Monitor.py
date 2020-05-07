from collections import deque
from multiprocessing import Process
import os
import time

class Monitor:

    def __init__(self):
        self.treads_queue = deque()

    def lock(self):
        while( len(self.treads_queue) != 0):
            id_tread = self.treads_queue.pop()
            print("push",id_tread)
            self.treads_queue.appendleft(id_tread)
            if( id_tread != os.getpid() ):
                time.sleep(1)
    
    def unlock(self):
        if(len(self.treads_queue) != 0):
            print("pop", self.treads_queue.pop())

    def size_treads_queue(self):
        return len(self.treads_queue)

    def enqueue(self, thread):
        self.treads_queue.append(thread)
        #print("push_id:", thread)

    def dequeue(self, thread):
        pass