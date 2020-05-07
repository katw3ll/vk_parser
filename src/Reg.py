import winreg
from winregistry import WinRegistry as Reg

def writeReg(data):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\vkparser",0,winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, "temp", 0, winreg.REG_SZ, data)
    key.Close()

def readReg():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\vkparser",0,winreg.KEY_ALL_ACCESS)
    val = winreg.QueryValueEx(key, "temp")
    key.Close()
    return val[0]

def lockRegLocker(name_locker):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\vkparser",0,winreg.KEY_ALL_ACCESS)
    val = int(winreg.QueryValueEx(key, name_locker)[0])
    val += 1
    winreg.SetValueEx(key, name_locker, 0, winreg.REG_SZ, str(val))
    key.Close()

def unlockRegLocker(name_locker):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\vkparser",0,winreg.KEY_ALL_ACCESS)
    val = int(winreg.QueryValueEx(key, name_locker)[0])
    val -=1
    winreg.SetValueEx(key, name_locker, 0, winreg.REG_SZ, str(val))
    key.Close()

def initRegLocker(name_locker):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\vkparser",0,winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, name_locker, 0, winreg.REG_SZ, "-1")
    key.Close()

def readRegLocker(name_locker):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\vkparser",0,winreg.KEY_ALL_ACCESS)
    val = int(winreg.QueryValueEx(key, name_locker)[0])
    key.Close()
    return val

def initReg():
    reg = Reg()
    if "vkparser" in reg.read_key(r'HKEY_CURRENT_USER\SOFTWARE')['keys']:
        writeReg("none")
        return
    reg.create_key(r'HKEY_CURRENT_USER\SOFTWARE\vkparser')
    writeReg("none")
