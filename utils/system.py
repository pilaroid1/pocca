import sys
import subprocess
import time
import os
import socket
import urllib.request
import configparser

class System():
    def __init__(self, update=True, supervisor_file="/media/usb/apps.conf"):
        if os.geteuid() == 0:
            self.info = {}
            self.supervisor_file = supervisor_file
            self.update = update
            self.getSupervisorSettings()
            if(self.update):
                self.getHostname()
                self.getIP()
                self.getSSID()
                self.getWiFi()
                self.getInternet()
                self.getDevMode()
                self.getApps()
        else:
            raise Exception("Need Root Permissions, try using sudo")

    def getSupervisorSettings(self):
        self.supervisor = configparser.ConfigParser()
        self.supervisor.read("/media/usb/apps.conf")

    def getApps(self):
        self.info["current_app"] = self.supervisor["program:app"]["command"].split("python")[1].split(".py")[0].strip()
        self.info["apps"] = []
        self.info["apps_in_use"] = []

        for section in self.supervisor.sections():
            self.info["apps_in_use"].append(self.supervisor[section]["command"].split("python")[1].split(".py")[0].strip())

        for dir in os.listdir("/media/usb/apps/"):
            self.info["apps"].append(dir)
        for dir_in_use in self.info["apps_in_use"]:
            self.info["apps"].remove(dir_in_use)

    def getDevMode(self):
        devmode = subprocess.check_output(["/media/usb/apps/pocca/utils/isdev.sh"])
        self.info["devmode"] = bool(devmode.decode().strip())

    def getHostname(self):
        self.info["hostname"] = socket.gethostname()

    def getIP(self):
        ip = subprocess.check_output(["hostname", "-I"])
        ip = ip.decode()
        ip = ip.split(" ")[0]
        self.info["ip"] = ip

    def getSSID(self):
        ssid = subprocess.check_output(["iwgetid", "-r"])
        self.info["ssid"] = ssid.decode().strip()

    def getWiFi(self):
        wifi_state = subprocess.check_output(["/media/usb/apps/pocca/utils/checkwifi.sh"])
        if "UP" in wifi_state.decode():
            self.wifi = True
        elif "DOWN" in wifi_state.decode():
            self.wifi = False

    def getInternet(self):
        try:
            urllib.request.urlopen("https://wikipedia.org")
            self.info["internet"] = True
        except:
            self.info["internet"] = False

    def info(self):
        return self.info

    # https://stackoverflow.com/questions/19813376/change-an-user-password-on-samba-with-python
    def change_samba_user(self, username, password):
        proc = subprocess.Popen(['smbpasswd', '-a', username], stdin=subprocess.PIPE)
        proc.communicate(input=password.encode() + '\n'.encode() + password.encode() + '\n'.encode())

    def change_ssh_user(self, username, password):
        pass_ssh = "\""+username+":"+password+"\""
        os.system("echo " + pass_ssh + " | chpasswd")

    def change_wifi(self):
        child = subprocess.Popen(["pkill", "wpa_supplicant"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(child.stdout.read().decode())
        time.sleep(1)
        child = subprocess.Popen(["wpa_supplicant", "-B", "-i","wlan0", "-c","/etc/wpa_supplicant/wpa_supplicant.conf"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(child.stdout.read().decode())

    def change_name(self, name):
        os.system("hostname " + self.info.name)
        os.system("systemctl restart avahi-daemon")
        os.system("systemctl restart nmbd")
