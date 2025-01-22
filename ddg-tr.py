'''
To Do:
Add option to skip download?
Clean up duplicate domains
Include CNAMEs
    - update requirements
    - test difference in file entries 
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
parser.add_argument('-c', '--cname', action='store_true', help="Exclude CNAME resolutions")
parser.add_argument('-s', '--skipdownload', action='store_true', help="Skip download. Requires domain CSV to already be present. Mostly used for testing")
args = vars(parser.parse_args())


# Set global variables based on arguments
domainDirectory = args["domaindirectory"]
domainCSV = domainDirectory / "domains.csv"
listDirectory = args["listdirectory"]
exclusionList = args["exclude"]
excludCNAMEs = args["cname"]
skipDownload = args["skipdownload"]

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
    if not skipDownload:
        getDomains(str(domainDirectory), domainCSV)
    search = Searcher(domainCSV)

    # Make lists for all the categories and include CNAMEs (if not excluded)
    for category in categories:
        if category not in exclusionList:
            categoryDF = search.searchCategory(category, exclusionList)
            if not excludCNAMEs:
                categoryDF = search.getCNAMEs(categoryDF)
            fileName = listDirectory / "{}.txt".format(category)
            writeDFtoList(categoryDF.df, category, fileName)

    # Make lists for all the fingerprinting levels and include CNAMEs (if not excluded)
    for i in range(4):
        fingerprintDF = search.searchFingerprint(i, exclusionList)
        if not excludCNAMEs:
            fingerprintDF = search.getCNAMEs(fingerprintDF)
        fileName = listDirectory / "Fingerprint-{}.txt".format(i)
        writeDFtoList(fingerprintDF.df, "Fingerprint-{}".format(i), fileName)

main()
