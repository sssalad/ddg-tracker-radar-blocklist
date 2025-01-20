#import pandas
from datetime import datetime, timezone


def getFileHeader(name, count):
    fileHeader = '''# Name: {}
# Last Updated: {}
# Domain Count: {}

# This list is based off of domains found in Duck Duck Go's Tracker Radar: https://github.com/duckduckgo/tracker-radar
# For more details on how this list was generated, visit: https://github.com/sssalad/ddg-tracker-radar-blocklist


'''.format(name, datetime.now(timezone.utc), count)

    return fileHeader


def writeDFtoList(df, listName, outputFile):
    with open(outputFile, "w") as f:
        rowCount = len(df.index)
        f.write(getFileHeader(listName, rowCount))

        for index, row in df.iterrows():
            f.write("0.0.0.0 " + row['domain'] + "\n")