#!/usr/bin/python3

'''Получение сведений о камере подключенной к регистратору из /ISAPI/System/deviceInfo

# ПЕРЕДАВАЕМЫЕ ПАРАМЕТРЫ
1-Имя/параметр  регистратора (как указано в файле settings.ini)
2-Тэг значение которого мы ищем
3-ID камеры на регистраторе
Возможные значения тэгов можно просмотреть в браузере на странице
/ISAPI/System/deviceInfo
/ISAPI/System/status

'''

import requests
import sys
import readinifile as readini
from xml.etree import cElementTree as ET
import getxml as getxml


deviceName = sys.argv[1]
deviceParameter = sys.argv[2]
channel_ID = sys.argv[3]

root = getxml.get_xml_fromdevice(deviceName, readini.getsettings('namespace', 'channels') + channel_ID + '/status')

# Эти данные мы получаем непосредственно с регистратора
if (deviceParameter == 'online') or (deviceParameter == 'ipAddress'):
	print(root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + deviceParameter).text.strip())
	sys.exit()
elif deviceParameter == 'deviceName':
	root = getxml.get_xml_fromdevice(deviceName, readini.getsettings('namespace', 'channels') + channel_ID)
	print(root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + 'name').text.strip())
	sys.exit()
elif (deviceParameter == 'model') or (deviceParameter == 'serialNumber') or (deviceParameter == 'firmwareVersion'):
	topage = '/ISAPI/System/deviceInfo'
else:
	topage = '/ISAPI/System/status'

# Следующие данные берем из камеры
# По ID номеру получим IP адрес камеры и обратимся непосредственно к камере

ipcam = (root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + 'ipAddress').text.strip())

r = requests.get('http://' + ipcam + topage, auth=(readini.getlogin(ipcam), readini.getpassword(ipcam)), stream=True)
root = ET.fromstring(r.text)
try:
	print(root.find('.//{http://www.isapi.org/ver20/XMLSchema}' + deviceParameter).text.strip())
except AttributeError:
	print(root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + deviceParameter).text.strip())