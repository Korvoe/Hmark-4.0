import configparser
import os
import sys
import json

class getConfig:
    nvdUrlBase  = ''
    nvdRSSUrl   = ''
    nvdRssAnalUrl   = ''
    dbuser      = ''
    dbpw        = ''
    dbhost      = ''
    dbport      = ''
    queuedb     = ''
    dbname      = ''
    dbcharset   = ''
    term        = ''
    workingDir  = ''
    vcsJson     = ''
    chromeDir   = ''
    gitRepoDir  = ''
    svnRepoDir  = ''
    diffDir     = ''

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'config.ini'))

        getConfig.nvdUrlBase    = config['URL']['nvdurl']
        getConfig.nvdRSSUrl     = config['URL']['nvdrssurl'] 
        getConfig.nvdRssAnalUrl = config['URL']['nvdRssAnalUrl']

        getConfig.dbuser        = config['DATABASE']['username']
        getConfig.dbpw          = config['DATABASE']['password']
        getConfig.dbhost        = config['DATABASE']['host']
        getConfig.dbport        = config['DATABASE']['port']
        getConfig.dbname        = config['DATABASE']['db_name']
        getConfig.dbcharset     = config['DATABASE']['charset']

        getConfig.term          = int(config['UPDATE']['term'])

        getConfig.workingDir    = config['DIR']['workingDir']
        getConfig.chromeDir     = config['DIR']['chromeDir']

        dataDir = os.path.join(getConfig.workingDir, "data")
        repoDir = os.path.join(dataDir, "repo")
        
        getConfig.gitRepoDir  = os.path.join(repoDir, "gitrepo")
        getConfig.svnRepoDir  = os.path.join(repoDir, "svnrepo")
        getConfig.diffDir     = os.path.join(dataDir, "diff")

        repos = os.path.join(getConfig.workingDir, "VCSList.json")
        with open(repos, 'r', encoding='UTF8') as f:
            getConfig.vcsJson = json.load(f)

    def check_vendor_product(self, vendor, product):
        for key, vcs in self.vcsJson.items():
            if vendor == vcs['vendor'] and product == vcs['product']:
                return True
        return False

    def get_repo_name(self, vendor, product):
        for key, vcs in self.vcsJson.items():
            if vendor == vcs['vendor'] and product == vcs['product']:
                return vcs['repo_name']
        return False

    def update_json(self):
        repos = os.path.join(getConfig.workingDir, "VCSList.json")
        with open(repos, 'w', encoding='UTF8') as f:
            f.seek(0)
            json.dump(getConfig.vcsJson, f, indent=4)
            f.truncate()