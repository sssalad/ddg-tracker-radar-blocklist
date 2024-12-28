import fsspec
from pathlib import Path
import requests
import zipfile
from domainDataFrame import DomainDataFrame

localFolder = Path.home() / "Documents/ddg-tracker-radar-blocklist/domains/"
baseURL = 'https://raw.githubusercontent.com/duckduckgo/tracker-radar/refs/heads/main/'

def downloadDomainsGitHub():
    localDestination = localFolder

    localDestination.mkdir(exist_ok=True, parents=True)
    fs = fsspec.filesystem("github", org="duckduckgo", repo="tracker-radar")
    fs.get(fs.ls("domains/"), localDestination.as_posix())

    for folder in localDestination.iterdir():
        #print("Downloading " + folder.stem + " domains")
        localSubFolder = localFolder.joinpath(folder.stem)
        #print(folder.stem)
        fs.get(fs.ls("domains/" + str(folder.stem)), localSubFolder.as_posix())

def fetchDomains():
    ddf = DomainDataFrame()

    # Get list of regions
    fs = fsspec.filesystem("github", org="duckduckgo", repo="tracker-radar")
    regions = (fs.ls("domains/", details=False))

    # For each domain in each region, add it to the data frame 
    for region in regions:
        print(region)
        for domain in fs.ls(region, details=False):
            url = (baseURL + "/" + domain)
            try:
                resp = requests.get(url)
                data = resp.json()
            except:
                print("URL Failed: " + url)

            input = [data['domain'], data['owner'], data['prevalence'], data['fingerprinting'],
                     data['cookies'], data['categories'], data['cnames']]
            ddf.appendDomain(input)
    return ddf




def downloadDomainsZIP():
    zipURL = 'https://github.com/duckduckgo/tracker-radar/archive/refs/heads/main.zip'
    response = requests.get(zipURL, stream=True)

    with open("tracker-radar.zip", mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            print("Writing another chunk")
            file.write(chunk)
    
    # Extract the zip
    with open("tracker-radar.zip", 'r') as zip_ref:
        zip_ref.extractall('tracker-radar')

    # Move to the universal download folder 
    

downloadDomainsZIP()