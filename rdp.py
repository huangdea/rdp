import os
import socket
import getpass
import winreg as reg

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP

def get_logged_in_username():
    return getpass.getuser()

def get_desktop_or_script_path():
    try:
        # 注册表获取桌面路径
        key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                          r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders',
                          0, reg.KEY_READ)
        path, _ = reg.QueryValueEx(key, 'Desktop')
        expanded_path = os.path.expandvars(path)
        if os.path.exists(expanded_path):
            return expanded_path
    except EnvironmentError:
        pass
    finally:
        try:
            reg.CloseKey(key)
        except:
            pass

    # 返回脚本所在的路径
    return os.path.dirname(os.path.realpath(__file__))



def create_rdp_file(ip, username,hostname):
    filename = f"{get_desktop_or_script_path()}\{hostname}-{username}.rdp" 
    content = f"""screen mode id:i:2
use multimon:i:0
desktopwidth:i:1920
desktopheight:i:1080
session bpp:i:24
winposstr:s:0,3,0,0,800,600
full address:s:{ip}
username:s:{username}
autoreconnection enabled:i:1
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:7
displayconnectionbar:i:1
disable wallpaper:i:1
allow font smoothing:i:1
allow desktop composition:i:0
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:1
disable cursor setting:i:0
bitmapcachepersistenable:i:1"""

    with open(filename, "w") as f:
        f.write(content)

    sys_command = f"ipconfig/all >> {get_desktop_or_script_path()}\ip-{hostname}-{username}.txt"
    os.system(sys_command)

hostname = socket.gethostname() #主机名
ip = get_local_ip() #ip
username = get_logged_in_username() #登录名
create_rdp_file(ip, username,hostname)
