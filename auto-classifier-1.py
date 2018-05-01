import os
import time
import pyshark
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing, cross_validation, neighbors

DATA_FOLDER = "data/"
DATA_PATH= "/Users/ranjininarayan/Desktop/18-750/wifi_fingerprinting/5G data/"
'''
Features in the classifier: 
-RSSI value 
-Address 
'''


class AccessPoint:
	def __init__(self, channel, address):
		self.channel = channel
		self.address = address
		self.weight = 0
		self.packets = []
		self.rssi_values = []

	def __str__(self):
		return self.address

	def addPacket(self, packet):
		self.weight += 1
		self.packets.append(packet)
		self.rssi_values.append(packet.wlan_radio.signal_dbm)

	def getRSSIList(self):
		return self.rssi_values

	def getPacketList(self):
		return self.packets


class Spectrum:
	def __init__(self):
		self.accessPoints = {}

	def __str__(self):
		output = "Spectrum:\n"
		for ap in self.accessPoints:
			output += "  " + ap.__str__() + "/n"
			for rssi in rssi_values:
				output += "    " + rssi + "\n"
		return output

	def addPacket(self, packet):
		address = packet.wlan.sa
		channel = packet.wlan_radio.channel
		rssi = packet.wlan_radio.signal_dbm

		if not address in self.accessPoints:
			ap = AccessPoint(channel, address)
			self.accessPoints[address] = ap

		self.accessPoints[address].addPacket(packet)
		address = ''.join(c for c in address if c.isalnum())
		address = int(address, 16)
		x = np.array([address, int(rssi)])
		#print x
		return x


class Inputs: 
	def __init__(self): 
		self.spectrum = Spectrum() 
		self.train = []
		self.len = 0

	def populate(self, f): 
		print f
		pcap = pyshark.FileCapture(f)
		print "here again"
		c = 0 
		for p in pcap: 
			#print (p.number)
			c += 1 
			x = self.spectrum.addPacket(p)
			if (len(x) == 2):
				self.train.append(x)
			# if c == 400:
			# 	break
		self.len = len(self.train)

class Classifier(): 
	def __init__(self): 
		self.X = []
		self.y = []

	def add_data(self, inputs, count): 
		self.X.extend(np.array(inputs.train))
		self.y.extend(np.full(inputs.len, count, dtype=int))

	def classify(self): 
		print self.X
		print len(self.y)
		X_train, X_test, y_train, y_test = cross_validation.train_test_split(self.X, self.y, test_size=0.2)
		clf = neighbors.KNeighborsClassifier()
		clf.fit(X_test, y_test)
		accuracy = clf.score(X_test, y_test)
		print accuracy

count = 0  
classify = Classifier() 
for (_, dirnames, _) in os.walk(DATA_PATH): 
	for folder in dirnames: 
		if "donner" in folder: 
			path = DATA_PATH+folder+"/data/"
			for (_, _, files) in os.walk(path):
				count += 1
				for f in files: 
					if f.endswith(".pcap"):
						inputs = Inputs() 
						print path+f
						inputs.populate(path+f) 
						classify.add_data(inputs, count)

classify.classify()	

                    