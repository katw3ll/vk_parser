import time
from src.Reg import lockRegLocker, unlockRegLocker, readRegLocker, initRegLocker

class Semaphore:
    def __init__(self, locker_name):
        self.locker_name = locker_name
        initRegLocker(self.locker_name)

    def lock(self):
        lockRegLocker(self.locker_name)
        while readRegLocker(self.locker_name) > 0:
           time.sleep(1)
    
    def unlock(self):
        unlockRegLocker(self.locker_name)