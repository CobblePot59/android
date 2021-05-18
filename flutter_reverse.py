import platform
import os
import codecs

def prerequisites():
    command = "os.system('java -version')"
    if not command:
        print('Please install java')
    else:
        reverse()

def reverse():
    global apk
    apk = input("Enter the name of your apk : ")
    version = "apktool_2.4.0.jar"
    apktool = "https://bitbucket.org/iBotPeaches/apktool/downloads/" + version

    if platform.system() == "Windows":
            os.system('powershell -c Invoke-WebRequest -Uri ' + apktool + ' -OutFile ' + version)
            os.system('java -jar ' + version +  ' d ' + apk)
            get_code()
    else:
            os.system('curl ' + apktool + ' -o ' + version)
            os.system('java -jar ' + version +  ' d ' + apk)
            get_code()

def get_code():
    unzip_apk = apk.split('.apk')[0]
    manifest = open(unzip_apk+'/AndroidManifest.xml', 'r', encoding='utf-8')
    m_content = manifest.read()
    name = m_content.split('package=')[1].split(' ')[0].strip('\"')
    short_name = name.split('.')[2]

    code = codecs.open('code.txt', 'a', 'ANSI')
    ifile = open(unzip_apk+'/assets/flutter_assets/kernel_blob.bin', 'r', encoding='ANSI')
    k_content = ifile.read()
    filter1 = k_content.split(short_name+'/lib')

    i=1
    while i < (len(filter1)-1):
        print(filter1[i], file=code)
        i+=1

    filter2 = filter1[len(filter1)-1].split('Copyright')
    print(filter2[0], file=code)  

prerequisites()