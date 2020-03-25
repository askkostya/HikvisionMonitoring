#!/usr/bin/python3
import requests
import sys
import readinifile as readini
from xml.etree import cElementTree as ET

if (sys.argv[2] == 'deviceType') or (sys.argv[2] == 'model') or (sys.argv[2] == 'firmwareVersion') or (
		sys.argv[2] == 'deviceName'):
	towwwpage = '/ISAPI/System/deviceInfo'
else:
	towwwpage = '/ISAPI/System/status'

r = requests.get('http://' + readini.getip(sys.argv[1]) + towwwpage,auth=(readini.getlogin(sys.argv[1]), readini.getpassword(sys.argv[1])), stream=True)
root = ET.fromstring(r.text)

try:
	print(root.find('.//{http://www.isapi.org/ver20/XMLSchema}' + sys.argv[2]).text.strip())
except AttributeError:
	print(root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + sys.argv[2]).text.strip())
