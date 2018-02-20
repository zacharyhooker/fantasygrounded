from phantasy import datahelper
import pprint
import os

def main():
    x = datahelper.DataHelper()
    for title, campaign in x.campaigns.items():
        outdir = os.path.join(os.path.dirname(__file__), 'render', title)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        if 'Princes' in title:
            characters = x.getCharacters(campaign)
            for name, charsheet in characters.items():
                outfile = os.path.join(outdir, name)
                x.renderData(charsheet, outfile, campaign.metadata['db.xml'])
                
    return 0

if __name__ == "__main__":
    main()
