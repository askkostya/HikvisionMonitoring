import requests
from xml.etree import cElementTree as ET
import readinifile as readini


def get_xml_fromdevice(devicename, namespace):
    r = requests.get(
        'http://' + readini.getip(devicename) + namespace,
        auth=(readini.getlogin(devicename), readini.getpassword(devicename)), stream=True)
    xmlstring = r.text
    root = ET.fromstring(xmlstring)
    return root
