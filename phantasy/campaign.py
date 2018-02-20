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
        self.dbdata = None

    @property
    def metadata(self):
        """Metadata for this specific campaign and database.
        Currently campaign.xml and db.xml.
        Including password, ruleset, username, root versioning... etc
        Returns:
            All data from campaign.xml and root meta from db.xml.
        """
        data = {}
        data['campaign.xml'] = utils.xmltodict(os.path.join(self.meta['dir'], 'campaign.xml'))
        data['db.xml'] = utils.xmltodict(os.path.join(self.meta['dir'], 'db.xml'))
        self.meta['campaign.xml'] = {}
        self.meta['db.xml'] = {}
        for key, values in data.items():
            if 'campaign' == key:
                self.meta[key] = values['root']
            else:
                self.meta[key]={k: v for k,v in data[key]['root'].items() if k.startswith('@')}
        return self.meta

    @property
    def data(self):
        """Data for this campaign. From db.xml
        Calls getData()
        
        Returns:
            Campaign's data
        """
        if self.dbdata:
            return self.dbdata
        else:
            self.dbdata = self.getData()
            return self.dbdata
        

    def getData(self, file_name = None):
        """Get data from the xml files in the directory. Currently grabs
        previous session dates and file information and the data dictionary 
        for the entire campaign.
        
        Args:
            file_name (optional): The file to grab the data from. (Eg.
            db.session, db.xml, db.backup data)
        
        Returns:
            Dictionary of data.
        """
        data = {}
        for rootdir, subdirs, files in os.walk(self.meta['dir']):
            for file in files:
                fullpath = os.path.join(rootdir, file)
                if file.endswith('.xml'):
                    xml = utils.xmltodict(fullpath)
                if 'db.session' in file:
                    epoch = int(file.split('.')[2])
                    date = datetime.fromtimestamp(epoch, timezone.utc).date()
                    self.sessions[file] = {'date': str(date), 'epoch': epoch}
                if file_name and filename in file:
                    data[file] = xml
                if 'db.xml' in file:
                    data[file] = xml
        if file_name:
            return data[file_name]
        return data['db.xml']

    @utils.checkAction
    def getAttribute(self, action, search = {}, file = None):
        """Get a particular attribute from the db.xml part of the dictionary.
        
        Args:
            action: Particular key to get. Must be set in actions.
            search (optional): Dictionary of subkeys and values to search.
            file (optional): Specify file if action in multiple files.
        
        Returns:
            A subset of the self.data dictionary for action key.
        """
        if not file:
            file = [k for k, v in self.actions.items() if action in v][0]
        data = self.data['root'][action]
        if len(search) > 0:
            for ret, value in data.items():
                print(ret)
                for key in search:
                    if key in value:
                        if search[key] in value[key]:
                            return data[ret]
        else:
            return data