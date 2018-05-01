import os
import signal
import time
import subprocess

CHANNELS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 36, 40, 44, 48, 149, 153, 157, 161, 165]
TIME_PER_CHANNEL = 10
TMP_PATH = "/private/tmp/"



for channel in CHANNELS:
    print("Sniffing channel %i" % channel)
    p = subprocess.Popen("airport sniff %i" % channel, shell=True)
    time.sleep(TIME_PER_CHANNEL)
    os.system("kill -INT %s" % p.pid)

print("Assembling results...")

airportFiles = ""

for (dirpath, dirnames, filenames) in os.walk(TMP_PATH):
    
    if dirpath == TMP_PATH:
        for f in filenames:
            if f.startswith("airportSniff") & f.endswith(".cap"):

                airportFiles += ("%s%s "%(TMP_PATH,f))

        airportFiles = airportFiles[:-1]

time.sleep(30)
os.system("sudo pkill airport")
os.system("mergecap -w output_wifi.cap %s"%airportFiles)

print("Moving source files to %sairportArchives..."%TMP_PATH)
os.system("mkdir %sairportArchives"%TMP_PATH)
os.system("mv %sairportSniff*.cap %sairportArchives"%(TMP_PATH,TMP_PATH))

os.system("tshark -r output_wifi.cap -T fields -e frame.number -e frame.time -e  wlan_radio.frequency -e wlan_radio.channel -e wlan_radio.signal_dbm -e ip.src -E separator=, -E quote=d -E header=y > hello.csv")