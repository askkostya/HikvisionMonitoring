#!/usr/bin/python3

import sys
import readinifile as readini
import getxml as getxml

deviceName = sys.argv[1]
deviceParameter = sys.argv[2]
channel_ID = sys.argv[3]

root = getxml.get_xml_fromdevice(deviceName, readini.getsettings('namespace', 'hddStatus') + channel_ID)

print(root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + deviceParameter).text.strip())
