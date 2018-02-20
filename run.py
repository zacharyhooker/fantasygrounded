from phantasy import datahelper
import pprint
import os

def main():
    x = datahelper.DataHelper()
    princes = None
    
    rootdata = {}
    rootdata['@version'] = '3.3'
    rootdata['@release'] = '8|CoreRPG:3'
    for campaign in x.campaigns:
        outdir = os.path.join(os.path.dirname(__file__), 'render', campaign)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        cmpgn = x.getCampaign(campaign)
        for name in x.getCharacters(cmpgn):
            charsheet = x.backupCharacter(cmpgn, name, outdir, rootdata)
    return 0

if __name__ == "__main__":
    main()
