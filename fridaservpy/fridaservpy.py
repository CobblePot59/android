import wget
import subprocess
import requests
import argparse
import lzma
import time
import frida

parser = argparse.ArgumentParser()
parser.add_argument("--arch", type = str, metavar = "<host>", help = "Specify type of architecture", choices=['arm', 'arm64', 'x86', 'x86_64'], default='x86_64')
args = parser.parse_args()

# Get the last version of frida-server for android with architecture specified
r = requests.get('https://api.github.com/repos/frida/frida/releases/latest').json()
version = r.get('tag_name')
arch = args.arch

for i in range (len(r.get('assets'))):
    if f'frida-server-{version}-android-{arch}.xz' in r.get('assets')[i].get('browser_download_url'):
        url = r.get('assets')[i].get('browser_download_url')

# Download frida-server.xz
wget.download(url, 'tmp/frida-server.xz')

# Decompress frida-server
with lzma.open('tmp/frida-server.xz', 'rb') as file:
    decompressed_data = file.read()

with open('tmp/frida-server', 'wb') as file:
    file.write(decompressed_data)

# Switch the device to root mode
subprocess.run("adb root", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Wait for the device
time.sleep(3)

# Push frida-server to the device's /data/local/tmp/
subprocess.run('adb push tmp/frida-server /data/local/tmp', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Set the appropriate permissions
subprocess.run('adb shell "chmod 755 /data/local/tmp/frida-server"', shell=True)

# Launch frida-server in background
print('\nfrida-server is started.')
subprocess.run('adb shell "nohup /data/local/tmp/frida-server > /dev/null 2>&1 &"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Get frida connected device
print(f'Device connected : {frida.get_usb_device()}')
