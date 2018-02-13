import winreg as reg
import os
from phantasy import campaign


class DataHelper:

    """A general helper for grabbing data from Fantasy Ground's
    Data folders.
    
    Attributes:
        dir_ (optional) : If None: derive the folder from the registry. Otherwise 
        use dir_ as the directory of the folder.
    """
    
    def __init__(self, dir_=None):
        if not dir_:
            dir_ = self.getDataDir()
        self.dir_ = dir_

    def getDataDir(self, version=None):
        """Grabs the FG/Data folder from the registry.
        
        Args:
            version (optional): Get a particular, if 
            multiple are installed, version's directory.
        
        Returns:
            Returns the data directory defined on config.
        """
        baseKey = reg.OpenKey(reg.HKEY_CURRENT_USER, 'Software\Fantasy Grounds')
        oldest = 0 if not version else version
        for i in range(reg.QueryInfoKey(baseKey)[0]):
            v = float(reg.EnumKey(baseKey, i))
            if v > oldest:
                oldest = v
            elif v == oldest:
                oldest = v
                break
        return reg.QueryValueEx(reg.OpenKey(baseKey, str(oldest)), 'DataDir')[0]

    @property
    def campaigns(self):
        """List all saved campaigns.
        
        Returns:
            List of campaigns by name.
        """
        fulldir = os.path.join(self.dir_, 'campaigns')
        #for campaign in next(os.walk(fulldir))[1]:
        return next(os.walk(fulldir))[1]

    def getCampaign(self, campaign_name):
        """Get the Campaign object based on campaign_name.
        This is usually just the Data directory with the campaign's name.
        
        Args:
            campaign_name: String title of the campaign. Can be found
            on the FG launch/load screen.
        
        Returns:
            Instance of campaign.
        """
        return campaign.Campaign(os.path.join(self.dir_, '/'.join(['campaigns', campaign_name])))