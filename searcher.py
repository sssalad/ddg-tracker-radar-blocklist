import pandas
from domainDataFrame import DomainDataFrame

class Searcher:
    def __init__(self, csvFile):
        self.df = pandas.read_csv(csvFile)

    def searchCategory(self, category, exclusionList):
        newDF = DomainDataFrame()

        for index, row in self.df.iterrows():
            if category in row['categories']:
                include = True
                for badCategory in exclusionList:
                    if badCategory in row['categories']:
                        include = False
                        break
                if include:
                    input = [row['domain'], row['owner'], row['prevalence'], row['fingerprinting'], 
                                   row['cookies'], row['categories'], row['cnames']]
                    newDF.appendDomain(input)

        return newDF.df