import unittest
from phantasy import campaign


class TestFG(unittest.TestCase):
	

	def test_campaigns(self):
    """
	There should be at least 1 campaign.
    """
    c = campaign.Campaign()
    self.assertEqual(len(c.campaigns)>0, True)


if __name__ == '__main__':
	unittest.main()