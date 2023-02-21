import argparse
import time
import subprocess


parser = argparse.ArgumentParser()

parser.add_argument("-H", type = str, metavar = "<host>", help = "Specify ip of the burp proxy server", required=True)
parser.add_argument("-P", type = str, metavar = "<port>", help = "Specify port of the burp proxy server", default=8080)

args = parser.parse_args()

PROXY_IP = args.H
PROXY_PORT = args.P

# Switch the device to root mode
subprocess.run("adb root", shell=True)

# Wait for the device
time.sleep(3)

# Remount the /system partition as read-write
subprocess.run("adb remount", shell=True)

# Push the certificate to the certificate store
subprocess.run("adb push 9a5ba575.0 /system/etc/security/cacerts/", shell=True)

# Set the appropriate permissions
subprocess.run("adb shell chmod 644 /system/etc/security/cacerts/9a5ba575.0", shell=True)
print("Burp Suite certificate installed successfully!")

# Change settings of device to redirect traffic to Burp Suite
subprocess.run('adb shell "' + f'settings put global http_proxy {PROXY_IP}:{PROXY_PORT}"', shell=True)
print("Device successfully connected to Burp Suite proxy!")
