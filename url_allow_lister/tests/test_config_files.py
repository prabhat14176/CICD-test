import os
import sys
import inspect
import unittest
import json
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
try:
    from application import loadConfigData
except ImportError:
    raise


class Test(unittest.TestCase):

    def setUp(self):
        self.domainsDict = loadConfigData()

    def test_isValidYaml(self):
        """
        test that the config files are valid yaml
        """
        success, _domainsDict, errorList = loadConfigData()
        self.assertTrue(success, json.dumps(errorList))

    def test_urlsHaveProtocol(self):
        """
        test that each url in the config file has the expected protocol
        """
        invalidUrls = []
        success, domainsDict, errorList = loadConfigData()
        self.assertTrue(success, json.dumps(errorList))
        for endpoint in domainsDict:
            self._testProtocols(domainsDict[endpoint])
        self.assertListEqual([], invalidUrls, 'Urls provided with no protocol: {}'.format(invalidUrls))

    def _testProtocols(self, domainsDict):
        """
        Cycle through each URL and check the protocol is correct.
        """
        for domain in domainsDict:
            invalidDomain = self._urlNotContainProtocol(domain)
            self.assertIsNone(invalidDomain, 'Url provided with no protocol: {}'.format(invalidDomain))

    @staticmethod
    def _urlNotContainProtocol(urlToCheck):
        """
        Does the given url contain http at the start
        """
        if not urlToCheck['URL'].lower().startswith('http'):
            return urlToCheck['URL']


if __name__ == "__main__":
    unittest.main()
