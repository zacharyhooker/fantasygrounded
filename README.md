# Fantasy Grounded
## Working title.

FantasyGrounded (PhantasY) is a project that helps utilize and explore data from the [Fantasy Grounds](https://www.fantasygrounds.com) application. Currently campaign data is supported including data available from previous sessions. As a DM and as a player I prefer to backup my character sheet after each session --  the first goal of this project is to automate character backups after each session. 

I will be working on merging [FGModGen](https://github.com/zacharyhooker/FGModGen) with this project to make a uniform module editor that can import and export data from existing sources. Once FGModGen is consolidated and the data folder is entirely accessible, other development resources will be implemented: rulesets, extensions, and distribution


## Installation

 1. Clone or download this repository into any Python-accessible location.
 2. Setup `run.py`to either search or read campaigns as below.



## Searching & Reading Campaign Data

 1. Pull data using the `datahelper.py`methods, or by directly accessing it through `campaign.py`.
 2. Use the included utils to convert the data from XML→Dict→🌈
 3. Render the data usable for [FGModGen](https://github.com/zacharyhooker/FGModGen) or readable by other processes.

## General Overview

Search through existing campaigns:

  from phantasy import datahelper
    data = datahelper.DataHelper()
    for campaign in x.campaigns:
      print(campaign)
Get metadata and data from a specific campaign:

    campaign = data.getCampaign('Basic Campaign')
    print(campaign.metadata, campaign.getData())

## Other Data Files

The other forms of data in the root folder, some of which are listed [here](http://www.fantasygrounds.com/wiki/index.php/Data_Files_Overview), will be implemented similarly.



## TODO

Documentation

 - ### Rulesets/Lua
   - FGModGen is currently ruleset agnostic although it can generate modules for specific rulesets. It is necessary to allow a larger scripting platform for the Lua implementation that SmiteWork's provides.
 - ### Extensions
   - Extensions (and most other FG files) are compressed files with scripting resources. The first order of FantasyGrounded's extension capabilities is to allow UI modifications. Think [FG Gap](https://www.fantasygrounds.com/forums/showthread.php?35819-Extension-5E-Theme-FG-GAP) and [BigFonts'](https://www.fantasygrounds.com/forums/showthread.php?25600-Using-FG-at-the-tabletop&p=227962&viewfull=1#post227962) XML font and graphics wrapping capabilities.
 - ### Distribution
   - Simple integration into the forum for posting and updating. 

