#!/usr/bin/python3

# Low level discovery script для обнаружения камер и накопителей в видеорегистраторах
# ПЕРЕДАВАЕМЫЕ ПАРАМЕТРЫ
# CAM - камеры подключенные к устройствам
# HDD - накопители подключенные к устройствам

import re
import requests
import sys
import readinifile as readini
from xml.etree import cElementTree as ET

deviceType = sys.argv[1]
if deviceType == 'HDD':
    towwwpage = '/ISAPI/ContentMgmt/Storage/hdd'
    rootxmltree = 'hdd'
if deviceType == 'CAM':
    towwwpage = '/ISAPI/ContentMgmt/InputProxy/channels/'
    rootxmltree = 'InputProxyChannel'

deviceList = readini.getonlynvrdevice()
jsondeviceid = ''
for i in range(len(deviceList)):
    r = requests.get('http://' + readini.getip(deviceList[i]) + towwwpage, auth=(readini.getlogin(deviceList[i]), readini.getpassword(deviceList[i])), stream=True)
    xmlstring = re.sub('\\sxmlns="[^"]+"', '', r.text, count=40)
    root = ET.fromstring(xmlstring)

    for deviceid in root.findall(rootxmltree):
        deviceid = deviceid.find('id').text
        jsondevicefind = ('{"{#DEVICEID}":"' + deviceid + '","{#NVRID}":"' + deviceList[i] + '"')
        jsondeviceid = jsondevicefind + '},' + jsondeviceid
jsondeviceid = jsondeviceid[0:-1]
print('{"data":[' + jsondeviceid + ']}')