from phantasy import datahelper
import pprint
import os

def main():
    x = datahelper.DataHelper()
    princes = None
    print(__file__)
    for campaign in x.campaigns:
        if campaign.startswith('Princes'):
            princes = x.getCampaign(campaign)
            break
    #pprint.pprint(princes.metadata, width=1)
    outdir = os.path.join(os.path.dirname(__file__), 'render')
    pprint.pprint(princes.getAttr('charsheet', {'name': 'Krug'}))
    return 0
    pprint.pprint(princes.renderData('charsheet', outdir, False))

if __name__ == "__main__":
    main()
