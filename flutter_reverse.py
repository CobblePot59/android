import subprocess
import requests
from urllib import request as dl
import codecs

def prerequisites():
    jdk = subprocess.run('java -version', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if jdk.returncode != 0:
        print('Please verify your java installation')
    else:
        reverse()

def reverse():
    global apk
    apk = input("Enter the name of your apk : ")
    r = requests.get('https://api.github.com/repos/iBotPeaches/Apktool/releases/latest')
    apktool = r.json()['assets'][0]['browser_download_url']
    
    print('Downloading...')
    dl.urlretrieve(apktool, 'apktool.jar')
    
    print('\nDecompiling...')
    subprocess.run('java -jar apktool.jar -f d ' + apk, shell=True)
    get_code()

def get_code():
    unzip_apk = apk.split('.apk')[0]
    manifest = open(unzip_apk+'/AndroidManifest.xml', 'r', encoding='utf-8').read()
    name = manifest.split('package=')[1].split(' ')[0].strip('\"')
    short_name = name.split('.')[2]

    code = codecs.open('code.txt', 'a', 'ANSI')
    ifile = open(unzip_apk+'/assets/flutter_assets/kernel_blob.bin', 'r', encoding='ANSI').read()
    filter1 = ifile.split(short_name+'/lib')

    i=1
    while i < (len(filter1)-1):
        print(filter1[i], file=code)
        i+=1

    filter2 = filter1[len(filter1)-1].split('Copyright')
    print(filter2[0], file=code)  

prerequisites()
