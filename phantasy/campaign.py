import os
from datetime import datetime, timezone
from phantasy import utils
import json

class Campaign:

    """Access and store campaign data from the FG Data folder.
    
    Attributes:
        dir_: The full directory of the campaign.
        meta: Temporary, immediate, metadata from dir string.
        sessions: A list of previous sessions.
    """
    
    def __init__(self, dir_):
        self.meta = {
            'dir': dir_,
            'name': os.path.basename(dir_)
        }
        self.sessions = {}

    @property
    def metadata(self):
        """Metadata for this specific campaign. (ie. Data fraom campaign.xml)
        Password, ruleset, username.
        Returns:
            Data from campaign.xml.
        """
        values = ['password', 'ruleset', 'username']
        data = utils.xmltodict(os.path.join(self.meta['dir'], 'campaign.xml'))
        self.meta['campaign.xml'] = {}
        for value in values:
            results = data['root'][value]
            self.meta['campaign.xml'][value] = results
        return self.meta

    def getData(self):
        """Get data from the xml files in the directory. Currently grabs
        previous session dates and file information and the data dictionary 
        for the entire campaign.
        """
        sessions = []
        for rootdir, subdirs, files in os.walk(self.meta['dir']):
            for file in files:
                fullpath = os.path.join(rootdir, file)
                if 'db.session' in file:
                    epoch = int(file.split('.')[2])
                    date = datetime.fromtimestamp(epoch, timezone.utc).date()
                    self.sessions[file] = {'date': str(date), 'epoch': epoch}
                if 'db.xml' in file:
                    data = utils.xmltodict(fullpath)
                    utils.renderXML(data['root']['charsheet'], 'this.xml')
                    utils.renderJSON(data['root']['charsheet'], 'this.json')
                    #return utils.renderJSON(data)
                    #self.parseCharacters(dbdict['root']['charsheet'])

    def parseCharacters(self, charsheet):
        """Beginnings of the character XML deconstruction.
        
        Args:
            charsheet: the XML etree Element of the entire, or a particular
            character sheet in campaign.xml.
        """
        for _, data in charsheet.items():
            print(data['name']['#text'], data['personalitytraits']['#text'])