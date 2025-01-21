'''
To Do:
Add option to skip download?
Clean up duplicate domains
Include CNAMEs
'''

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
parser.add_argument('-e','--exclude', nargs='*', default=["Badge", "CDN"], help="Exclude a category from all results")
args = vars(parser.parse_args())


# Set global variables based on arguments
domainDirectory = args["domaindirectory"]
domainCSV = domainDirectory / "domains.csv"
listDirectory = args["listdirectory"]
exclusionList = args["exclude"]

categories = ["Action Pixels", "Ad Fraud", "Ad Motivated Tracking", "Advertising", "Analytics" , 
              "Audience Measurement", "Badge", "CDN", "Embedded Content", "Federated Login", 
              "Malware", "Non-tracking", "Online Payment", "Obscure Ownership", "SSO", "Session Replay", 
              "Social Network", "Social - Comment", "Social - Share", "Tag Manager", 
              "Third-Party Analytics Marketing", "Unknown High Risk Behavior"]

def main():
    # Check that exclusion arguments are valid
    if (len(exclusionList) != 0):
        for item in exclusionList:
            if item not in categories:
                print("Invalid category exclusion argument. Check categories and make sure category exclusion arguments are wrapped in single quotes")
                sys.exit()

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
    getDomains(str(domainDirectory), domainCSV)
    search = Searcher(domainCSV)
    for category in categories:
        if category not in exclusionList:
            categoryDF = search.searchCategory(category, exclusionList)
            fileName = listDirectory / "{}.txt".format(category)
            writeDFtoList(categoryDF, category, fileName)

main()
