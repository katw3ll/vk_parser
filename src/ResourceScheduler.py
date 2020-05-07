from src.Semaphore import Semaphore
from src.MyThreads import ThreadWriter, ThreadReader
from src.Reg import writeReg, readReg
import time
from collections import deque

size_queue = 30

class ResourceScheduler:
    def __init__(self, config):
        self.semaphore_1 = Semaphore('lock1')
        self.semaphore_2 = Semaphore('lock2')
        self.semaphore_3 = Semaphore('lock3')
        self.config = config
        self.titles = dict()
        self.texts = dict()
        self.images = dict()
        self.table = deque()

    def do(self, thread_1, thread_2, thread_3):
        thread_1.start()
        thread_2.start()
        thread_3.start()
        # ---
        thread_1.join()
        thread_2.join()
        thread_3.join()

    def create_thread(self, id, data):
        if id == 1:
            return ThreadWriter(self.config['paths']['cache_file1'], self.semaphore_1, data)
        elif id == 2:
            return ThreadWriter(self.config['paths']['cache_file2'], self.semaphore_2, data)
        elif id == 3:
            return ThreadWriter(self.config['paths']['cache_file3'], self.semaphore_3, data)
        elif id == 4:
            return ThreadReader(self.config['paths']['cache_file1'], self.config['paths']['cache_file2'], \
                   self.config['paths']['cache_file3'], self.semaphore_1, self.semaphore_2, self.semaphore_3)
    
    def update_data(self, titles, texts, images):
        temp_titles = self.titles
        temp_texts = self.texts
        temp_images = self.images
        # ----
        self.titles = titles
        self.texts = texts
        self.images = images
        # ----
        if temp_titles:
            for key in temp_titles.keys():
                if key in self.titles.keys():
                    continue
                self.titles[key] = temp_titles[key]
        if temp_texts:
            for key in temp_texts.keys():
                if key in self.texts.keys():
                    continue
                self.texts[key] = temp_texts[key]
        if temp_images:
            for key in temp_images.keys():
                if key in self.images.keys():
                    continue
                self.images[key] = temp_images[key]
        
    def update_table(self):
        while len(self.table) < size_queue:
            self.table.append([1,2,3])
            self.table.append([5,5,5])
            self.table.append([4,2,3])
            self.table.append([5,5,5])
            self.table.append([1,4,3])
            self.table.append([5,5,5])
            self.table.append([1,2,4])
            self.table.append([5,5,5])

    def print_table(self):
        for t in self.table:
            print(t)

    def step(self):
        step = self.table.popleft()
        if step[0] < 5:
            thread_1 = self.create_thread(step[0], self.titles)
            thread_2 = self.create_thread(step[1], self.texts)
            thread_3 = self.create_thread(step[2], self.images)
            print("work", step)
            self.do(thread_1, thread_2, thread_3)
            if step[0] != 4:
                self.titles = dict()
            if step[1] != 4:
                self.texts = dict()
            if step[2] != 4:
                self.images = dict()
        
        if step[0] == 5:
            self.semaphore_1.lock()
            self.semaphore_2.lock()
            self.semaphore_3.lock()
            print("work other process")
            writeReg("do")
            while readReg() != "done":
                time.sleep(1)
            self.semaphore_1.unlock()
            self.semaphore_2.unlock()
            self.semaphore_3.unlock()
        self.update_table()

