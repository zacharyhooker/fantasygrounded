import unittest
import tempfile
from lxml import etree
import sys
sys.path.insert(0, '../')
from phantasy import datahelper, utils


class TestFG(unittest.TestCase):

    def test_campaigns(self):
        """
        Data dir should end with /Data/
        There should be at least 1 campaign.
        """
        c = datahelper.DataHelper()
        self.assertEqual(c.getDataDir().endswith('/Data/'), True)
        self.assertEqual(len(c.campaigns)>0, True)

    def test_xml(self):
        """
        Testing XML string/file->dict and dict->string/file encoding and decoding.
        """
        xmlstring = etree.tostring(etree.fromstring(b'<?xml version="1.0" encoding="UTF-8"?><zAppointments reminder="15"><appointment><begin>1181251680</begin><uid>040000008200E000</uid><alarmTime>1181572063</alarmTime><state /><location /><duration>1800</duration><subject>Bring pizza home</subject></appointment><appointment><begin>1234360800</begin><duration>1800</duration><subject>Check MS Office website for updates</subject><location /><uid>604f4792-eb89-478b-a14f-dd34d3cc6c21-1234360800</uid><state>dismissed</state></appointment></zAppointments>'))
        xmldict = {'zAppointments': {'appointment': [{'begin': '1181251680', 'uid': '040000008200E000', 'alarmTime': '1181572063', 'state': None, 'location': None, 'duration': '1800', 'subject': 'Bring pizza home'}, {'begin': '1234360800', 'duration': '1800', 'subject': 'Check MS Office website for updates', 'location': None, 'uid': '604f4792-eb89-478b-a14f-dd34d3cc6c21-1234360800', 'state': 'dismissed'}], '@reminder': '15'}}
        file = tempfile.NamedTemporaryFile('w', delete=False)
        file.write(xmlstring.decode())
        file.close()
        self.assertEqual(utils.xmltodict(file.name), xmldict)
        self.assertEqual(etree.tostring(utils._dicttoxml(xmldict)), xmlstring)


if __name__ == '__main__':
    unittest.main()