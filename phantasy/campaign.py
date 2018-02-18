import os
from datetime import datetime, timezone
from phantasy import utils
import json

class Campaign:
    root_attribs = {}
    actions = {'db.xml':['charsheet', 'feat']}

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

    def getData(self, file_name):
        """Get data from the xml files in the directory. Currently grabs
        previous session dates and file information and the data dictionary 
        for the entire campaign.
        """
        sessions = []
        data = {}
        for rootdir, subdirs, files in os.walk(self.meta['dir']):
            for file in files:
                fullpath = os.path.join(rootdir, file)
                data = {}
                if file.endswith('xml'):
                    data = utils.xmltodict(fullpath)
                if 'db.xml' in file:
                    for key, value in data['root'].items():
                        if key.startswith('@'):
                            self.root_attribs[key] = value
                if 'db.session' in file:
                    epoch = int(file.split('.')[2])
                    date = datetime.fromtimestamp(epoch, timezone.utc).date()
                    self.sessions[file] = {'date': str(date), 'epoch': epoch}
                if file_name in file:
                    return data
        return data

    @utils.checkAction
    def getAttribute(self, action, search = [], file = None):
        if not file:
            file = [k for k, v in self.actions.items() if action in v][0]
        data = self.getData(file)['root'][action]
        if len(search) > 0:
            for ret, value in data.items():
                for key in search:
                    if key in value:
                        if search[key] in value[key]['#text']:
                            return data[ret]
        else:
            return data