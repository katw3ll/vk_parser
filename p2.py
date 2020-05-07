from src.JsonTool import JsonTool
from src.Reg import *
from multiprocessing import Process
import sqlite3, time

config = JsonTool.parse("config.json")

conn = sqlite3.connect("db.sqlite3") 
cursor = conn.cursor()

initReg()

_id = []

class DataBaseWriter(Process):
    def __init__(self, data, request):
        Process.__init__(self)
        self.data = data
        self.request = request

    def run(self):
        global conn
        global cursor
        cursor.execute("SELECT id FROM posts")
        res = cursor.fetchall()
        for i in res:
            _id.append(i[0])
        for key in self.data.keys():
            if key in _id:
                sql = "UPDATE posts SET "+self.request+"=(?) WHERE id=(?)"
                cursor.execute(sql, (str(self.data[key]),key))
            else:
                sql = "INSERT INTO posts(id,"+self.request+") VALUES (?, ?)"
                cursor.execute(sql, (key, str(self.data[key])))
                _id.append(key)
        conn.commit()


if __name__ == '__main__':
    while True:
        while readReg() != "do":
            time.sleep(1)
        titles = JsonTool.parse(config['paths']['cache_file1'])
        texts = JsonTool.parse(config['paths']['cache_file2'])
        images = JsonTool.parse(config['paths']['cache_file3'])
        thread_1 = DataBaseWriter(titles, 'title')
        thread_2 = DataBaseWriter(texts, 'text')
        thread_3 = DataBaseWriter(images, 'images')

        thread_1.start()
        thread_1.join()
        thread_2.start()
        thread_2.join()
        thread_3.start()
        thread_3.join() 
         
        print("DB update")
        writeReg("done")



#print(main_dict)


