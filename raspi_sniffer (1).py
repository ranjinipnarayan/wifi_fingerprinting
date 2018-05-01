import os
from scapy.all import *

CHANNELS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 36, 40, 44, 48, 149, 153, 157, 161, 165]
OUTPUT_NAME = "donner025"

os.system("sudo ifconfig wlan1 down")
os.system("sudo iwconfig wlan1 mode monitor")
os.system("sudo ifconfig wlan1 up")

for channel in CHANNELS:
    print("Sniffing channel %i" % channel)
    os.system("sudo iwconfig wlan1 channel %s" % channel)
    os.system("touch %s_channel_%i.pcap" % (OUTPUT_NAME, channel))
    os.system("chmod o=rw %s_channel_%i.pcap" % (OUTPUT_NAME, channel))
    # uses tshark to write sniff traces to file, can filter packets included
    os.system("sudo tshark -i wlan1 -c 100 -w %s_channel_%i.pcap" % (OUTPUT_NAME, channel))
    os.system("tshark -r %s_channel_%i.pcap" % (OUTPUT_NAME, channel))

# this uses scapy which would be nicer than tshark but idk how to use it well
#sniff(iface="wlan1", count=1, prn=lambda x: x.show())