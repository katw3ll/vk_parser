from multiprocessing import Process
from src.Semaphore import Semaphore
from src.JsonTool import JsonTool
import os, time


class ThreadWriter(Process):
    def __init__(self, filename, semaphore, data):
        Process.__init__(self)
        self.filename =  filename
        self.semaphore = semaphore
        self.data = data
    
    def run(self):
        self.semaphore.lock()
        temp_file = JsonTool.parse(self.filename)
        #print(self.data)
        for key in self.data.keys():
            if key in temp_file.keys():
                continue
            temp_file[key] = self.data[key]
        JsonTool.save_to_file(self.filename, temp_file)
        self.semaphore.unlock()

class ThreadReader(Process):
    def __init__(self, filename_1, filename_2, filename_3, semaphore_1, semaphore_2, semaphore_3):
        Process.__init__(self)
        self.filename_1 =  filename_1
        self.filename_2 =  filename_2
        self.filename_3 =  filename_3
        self.semaphore_1 = semaphore_1
        self.semaphore_2 = semaphore_2
        self.semaphore_3 = semaphore_3

    def run(self):
        self.semaphore_1.lock()
        JsonTool.parse(self.filename_1) 
        self.semaphore_1.unlock()
        self.semaphore_2.lock()
        JsonTool.parse(self.filename_2) 
        self.semaphore_2.unlock()
        self.semaphore_3.lock()
        JsonTool.parse(self.filename_3) 
        self.semaphore_3.unlock()

