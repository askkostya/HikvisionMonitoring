#!/usr/bin/python3
import configparser

config = configparser.ConfigParser()
config.read('/home/pi/scripts/settings.ini')


def getip(cameraname):
	return config.get(cameraname, "ip")


def getlogin(cameraname):
	return config.get(cameraname, "login")


def getpassword(cameraname):
	return config.get(cameraname, "password")


def getdevicetype(devicetype):
	return config.get(devicetype, "deviceType")


def getsettings(section, value):
	return config.get(section, value)


def getonlynvrdevice():
	deviceList = []
	fsect = config.sections()
	for i in range(len(fsect)):
		if getdevicetype(fsect[i]) == "NVR":
			deviceList.append(fsect[i])
	return deviceList
