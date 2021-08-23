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
            self.refresh = update
            self.getSupervisorSettings()
            if(self.refresh):
                self.update()
        else:
            raise Exception("Need Root Permissions, try using sudo")

    def update(self):
        self.getHostname()
        self.getIP()
        self.getSSID()
        self.getWiFi()
        self.getInternet()
        self.getDevMode()
        self.getApps()
        self.getScreen()

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

    def getScreen(self):
        self.info["screen"] = None
        self.info["screen_resolution"] = (320,240)
        f = open("/boot/config.txt", "r")
        lines = f.readlines()
        for line in lines:
            if "dtoverlay" in line and "#dtoverlay" not in line and "fps" in line:
                self.info["screen"] = line.strip().split("dtoverlay=")[1].split(",")[0]
        if self.info["screen"] == "pitft22":
            self.info["screen_resolution"] = (320,240)

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
        return ip

    def getSSID(self):
        try:
            ssid = subprocess.check_output(["iwgetid", "-r"])
            self.info["ssid"] = ssid.decode().strip()
        except:
            print("Wifi is disconnected")
            self.info["ssid"] = ""

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

    def change_app(self, app_name):
        # If app_name.py file exists
        if os.path.isfile("/media/usb/apps/" + app_name + "/" + app_name + ".py"):
            # change application in supervisor
            self.supervisor["program:app"]["command"] = "python " + app_name + ".py"
            self.supervisor["program:app"]["directory"] = "/media/usb/apps/" + app_name
            with open(self.supervisor_file, 'w') as configfile:
                self.supervisor.write(configfile)
            os.system("sudo supervisorctl update")
            os.system("sudo supervisorctl stop webapi")
            os.system("sudo supervisorctl start webapi")

    def change_name(self, name):
        f = open("/etc/hostname", "w")
        f.write(name)
        f.close()
        # Change name in /etc/hosts
        f = open("/etc/hosts", "r")
        lines = f.readlines()
        i = 0
        for line in lines:
            # If line contains 127.0.1.1
            if "127.0.1.1" in line:
                # Split line in two string
                lines[i] = "127.0.1.1   " + name + "\n"
            i += 1
        # Save lines in /etc/hosts
        f = open("/etc/hosts", "w")
        f.writelines(lines)
        f.close()

        os.system("hostname " + name)
        os.system("systemctl restart avahi-daemon")
