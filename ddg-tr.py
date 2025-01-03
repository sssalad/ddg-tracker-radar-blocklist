from pathlib import Path
from downloader import getDomains
from searcher import Searcher
from writer import writeDFtoList

domainDirectory = Path.home() / ".ddgtrbl"
domainCSV = domainDirectory / "domains.csv"

listDirectory = Path.cwd() / "lists"

categories = ["Action Pixels", "Ad Fraud", "Ad Motivated Tracking", "Advertising", "Analytics" , 
              "Audience Measurement", "Badge", "CDN", "Embedded Content", "Federated Login", 
              "Malware", "Non-tracking", "Online Payment", "Obscure Ownership", "SSO", "Session Replay", 
              "Social Network", "Social - Comment", "Social - Share", "Tag Manager", 
              "Third-Party Analytics Marketing", "Unknown High Risk Behavior"]

def main():
    domainDirectory.mkdir(exist_ok=True, parents=True)
    listDirectory.mkdir(exist_ok=True, parents=True)

    #getDomains('zip', str(domainDirectory))
    search = Searcher(domainCSV)
    for category in categories:
        categoryDF = search.searchCategory(category)
        fileName = listDirectory / "{}.txt".format(category)
        writeDFtoList(categoryDF, category, fileName)

main()
