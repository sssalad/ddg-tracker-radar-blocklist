'''
To Do:
Add better output to zip download, add percentage or something
'''

import fsspec
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

############################
### Downloader Functions ###
############################
def downloadDomainsHTML():
    ddf = DomainDataFrame()

    # Get list of regions
    fs = fsspec.filesystem("github", org="duckduckgo", repo="tracker-radar")
    regions = (fs.ls("domains/", details=False))

    # For each domain in each region, add it to the data frame 
    for region in regions:
        for domain in fs.ls(region, details=False):
            url = (githubBaseURL + "/" + domain)
            try:
                resp = requests.get(url)
                data = resp.json()
            except:
                print("URL Failed: " + url)

            input = [data['domain'], data['owner'], data['prevalence'], data['fingerprinting'],
                     data['cookies'], data['categories'], data['cnames']]
            ddf.appendDomain(input)
    return ddf

def downloadDomainsGitHub(localFolder):
    #localFolder.mkdir(exist_ok=True, parents=True)
    localFolder = Path(localFolder)
    fs = fsspec.filesystem("github", org="duckduckgo", repo="tracker-radar")
    fs.get(fs.ls("domains/"), localFolder.as_posix())

    for folder in localFolder.iterdir():
        #print("Downloading " + folder.stem + " domains")
        localSubFolder = localFolder.joinpath(folder.stem)
        #print(folder.stem)
        fs.get(fs.ls("domains/" + str(folder.stem)), localSubFolder.as_posix())

    #get dataframe
    ddf = readAllJson(localFolder)
    #cleanup files 

    return ddf

def downloadDomainsZIP(localFolder):
    response = requests.get(zipDownloadURL, stream=True)
    zipFile = localFolder + "/tracker-radar.zip"
    extractedZipFolder = localFolder + "/tracker-radar/"
    extractedDomainFolder = localFolder + "/tracker-radar/tracker-radar-main/domains/"

    with open(zipFile, mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            print("Writing another chunk")
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
def getDomains(getType, localFolder):
    outputFile = localFolder + "/domains.csv"

    if getType == 'html':
        ddf = downloadDomainsHTML()
    elif getType == 'github':
        ddf = downloadDomainsGitHub(localFolder)
    elif getType == 'zip':
        ddf = downloadDomainsZIP(localFolder)
    else:
        print("Error")
        return 0
    
    ddf.df.to_csv(outputFile, encoding='utf-8', index=False, header=True)