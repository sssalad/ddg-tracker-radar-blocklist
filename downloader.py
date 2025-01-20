'''
To Do:
Add better output to zip download, add percentage or something
'''

from pathlib import Path
import requests
import zipfile
import json
import shutil
from domainDataFrame import DomainDataFrame

githubBaseURL = 'https://raw.githubusercontent.com/duckduckgo/tracker-radar/refs/heads/main/'
zipDownloadURL = 'https://github.com/duckduckgo/tracker-radar/archive/refs/heads/main.zip'

########################
### Helper Functions ###
########################
def unzipFile(zipFile, destinationFolder):
    with zipfile.ZipFile(zipFile, 'r') as zip_ref:
        zip_ref.extractall(destinationFolder)

def readAllJson(localFolder):
    localFolder = Path(localFolder)
    ddf = DomainDataFrame()

    for folder in localFolder.iterdir():
        localSubFolder = localFolder.joinpath(folder.stem)
        for file in localSubFolder.glob('*.json'):
            with open(file, mode='r', encoding="utf-8") as read_file:
                data = json.load(read_file)
                input = [data['domain'], data['owner'], data['prevalence'], data['fingerprinting'],
                     data['cookies'], data['categories'], data['cnames']]
                ddf.appendDomain(input)
    return ddf

###########################
### Downloader Function ###
###########################
def downloadDomainsZIP(localFolder):
    response = requests.get(zipDownloadURL, stream=True)
    zipFile = localFolder + "/tracker-radar.zip"
    extractedZipFolder = localFolder + "/tracker-radar/"
    extractedDomainFolder = localFolder + "/tracker-radar/tracker-radar-main/domains/"

    with open(zipFile, mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            #print("Writing another chunk")
            file.write(chunk)
    
    # Extract the zip
    unzipFile(zipFile, extractedZipFolder)

    #get dataframe
    ddf = readAllJson(extractedDomainFolder)

    # Cleanup download files     
    shutil.rmtree(extractedZipFolder)
    Path.unlink(Path(zipFile))

    return ddf

#####################################################
### "Main" function that ties everything together ###
#####################################################
def getDomains(getType, localFolder, domainCSV):
    ddf = downloadDomainsZIP(localFolder)
    ddf.df.to_csv(domainCSV, encoding='utf-8', index=False, header=True)