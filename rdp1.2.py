import os
import socket
import getpass
import subprocess
from datetime import datetime
import sys
import winreg

def get_mstsc_port():
    try:
        # 打开注册表路径
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp", 0, winreg.KEY_READ)
        
        # 读取PortNumber值
        port, reg_type = winreg.QueryValueEx(reg_key, "PortNumber")
        
        # 关闭注册表键
        winreg.CloseKey(reg_key)
        
        return port
    except Exception as e:
        print(f"无法获取RDP端口，使用默认端口 3389. 错误: {e}")
        return 3389  # 如果获取失败，返回默认端口

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def get_logged_in_username():
    return getpass.getuser()

def get_executable_path():
    if hasattr(sys, "frozen"):  # 如果是打包后的可执行文件
        return os.path.dirname(sys.executable)
    else:  # 如果是通过脚本运行
        return os.path.dirname(os.path.realpath(__file__))

def create_rdp_and_ip_files(ip, username, hostname):
    current_date = datetime.now().strftime("%Y-%m-%d")
    executable_path = get_executable_path()  # 获取可执行文件的路径

    base_filename = f"{hostname}-{username}-{current_date}"
    rdp_filename = os.path.join(executable_path, f"{base_filename}.rdp")
    txt_filename = os.path.join(executable_path, f"{base_filename}.txt")

    mstsc_port = get_mstsc_port()

    rdp_content = f"""full address:s:{ip}:{mstsc_port}
username:s:{username}
drivestoredirect:s:*"""  # 挂载所有本地驱动器

    with open(rdp_filename, "w") as rdp_file:
        rdp_file.write(rdp_content)

    # 获取ipconfig /all的输出
    ipconfig_output = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True).stdout

    txt_content = f"RDP Port: {mstsc_port}\n\nIP Configuration:\n{ipconfig_output}"

    with open(txt_filename, "w") as txt_file:
        txt_file.write(txt_content)

def main():
    hostname = socket.gethostname()  # 获取主机名
    ip = get_local_ip()  # 获取本地IP地址
    username = get_logged_in_username()  # 获取登录用户名
    create_rdp_and_ip_files(ip, username, hostname)  # 创建RDP和TXT文件

    print("RDP和TXT文件已生成。")

if __name__ == "__main__":
    main()
