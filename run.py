from phantasy import datahelper
import pprint

if __name__ == "__main__":
	x = datahelper.DataHelper()
	princes = None
	for campaign in x.campaigns:
		if campaign.startswith('Princes'):
			princes = x.getCampaign(campaign)
			break
	#pprint.pprint(princes.metadata, width=1)
	print(princes.metadata)
	print(princes.getData())