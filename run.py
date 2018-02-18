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
    outdir = os.path.join(os.path.dirname(__file__), 'render')
    pprint.pprint(princes.getAttribute('charsheet', {'name': 'Krug'}))
    pprint.pprint(princes.getAttribute('feat', {'name': 'Great Weapon Master'}))
    #princes.rD(princes.getAttr('charsheet', {'name': 'Krug'}), outdir)
    return 0

if __name__ == "__main__":
    main()
