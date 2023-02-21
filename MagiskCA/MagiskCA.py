import time
import argparse
import subprocess


parser = argparse.ArgumentParser()

parser.add_argument("-H", type = str, metavar = "<host>", help = "Specify ip of the burp proxy server", required=True)
parser.add_argument("-P", type = str, metavar = "<port>", help = "Specify port of the burp proxy server", default=8080)

args = parser.parse_args()

PROXY_IP = args.H
PROXY_PORT = args.P

# Push the certificate to the device's /sdcard/
subprocess.run('adb push cacert.cer /sdcard/', shell=True)

# Change settings of device to redirect taffic to Burp Suite
subprocess.run('adb shell "' + f'settings put global http_proxy {PROXY_IP}:{PROXY_PORT}"', shell=True)
print("Device successfully connected to Burp Suite proxy!")

# Switch the device to root mode
subprocess.run("adb root", shell=True)

# Wait for the device
time.sleep(3)

# Launch Trust CA Installer Activity to install previous cert
subprocess.run('adb shell am start -n com.android.settings/.security.InstallCaCertificateWarning', shell=True)
print('Click on install on your device and select cacert.cer file, located in the sdcard')
input('Press enter when the task is finnish')

# Push Magisk extension to the device's /sdcard/
subprocess.run('adb push AlwaysTrustUserCerts.zip /sdcard/', shell=True)

# Launch Magisk Extension Installer Activity to install previous extension
subprocess.run('adb shell am start -n com.topjohnwu.magisk/.ui.MainActivity', shell=True)
print('Click on module > install on your device and select AlwaysTrustUserCerts.zip file, located in the sdcard, then click on reboot')
