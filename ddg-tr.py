from pathlib import Path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys

from downloader import getDomains
from searcher import Searcher
from writer import writeDFtoList


# Set arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-d', '--domaindirectory', default=(Path.home() / ".ddgtrbl"), help="Directory that domain data will be stored in")
parser.add_argument('-l', '--listdirectory', default=(Path.cwd() / "lists"), help="Directory that lists will be written to")
args = vars(parser.parse_args())


# Set global variables based on arguments
domainDirectory = args["domaindirectory"]
domainCSV = domainDirectory / "domains.csv"
listDirectory = args["listdirectory"]

categories = ["Action Pixels", "Ad Fraud", "Ad Motivated Tracking", "Advertising", "Analytics" , 
              "Audience Measurement", "Badge", "CDN", "Embedded Content", "Federated Login", 
              "Malware", "Non-tracking", "Online Payment", "Obscure Ownership", "SSO", "Session Replay", 
              "Social Network", "Social - Comment", "Social - Share", "Tag Manager", 
              "Third-Party Analytics Marketing", "Unknown High Risk Behavior"]

def main():
    # Create the needed directories if they don't already exist
    try:
        domainDirectory.mkdir(exist_ok=True, parents=True)
    except:
        print("Error creating domain directory. Make sure file path is valid and writable")
        sys.exit()

    try:
        listDirectory.mkdir(exist_ok=True, parents=True)
    except: 
        print("Error creating list directory. Make sure file path is valid and writable")
        sys.exit()

    # Do actual stuff 
    getDomains('zip', str(domainDirectory))
    search = Searcher(domainCSV)
    for category in categories:
        categoryDF = search.searchCategory(category)
        fileName = listDirectory / "{}.txt".format(category)
        writeDFtoList(categoryDF, category, fileName)

main()
