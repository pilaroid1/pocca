import sys
import subprocess
import time
import os
import socket

class System():
    def __init__(self):
        if os.geteuid() == 0:
            self.name = socket.gethostname()
            ip = subprocess.check_output(["hostname", "-I"])
            ip = ip.decode()
            ip = ip.split(" ")[0]
            self.ip = ip
        else:
            raise Exception("Need Root Permissions, try using sudo")

    # https://stackoverflow.com/questions/19813376/change-an-user-password-on-samba-with-python
    def update_samba_user(self, username, password):
        proc = subprocess.Popen(['smbpasswd', '-a', username], stdin=subprocess.PIPE)
        proc.communicate(input=password.encode() + '\n'.encode() + password.encode() + '\n'.encode())

    def update_ssh_user(self, username, password):
        pass_ssh = "\""+username+":"+password+"\""
        os.system("echo " + pass_ssh + " | chpasswd")

    def restart_wifi(self):
        child = subprocess.Popen(["pkill", "wpa_supplicant"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(child.stdout.read().decode())
        time.sleep(1)
        child = subprocess.Popen(["wpa_supplicant", "-B", "-i","wlan0", "-c","/etc/wpa_supplicant/wpa_supplicant.conf"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(child.stdout.read().decode())

    def change_name(self, name):
        os.system("hostname " + name)
        os.system("systemctl restart avahi-daemon")
        os.system("systemctl restart nmbd")
