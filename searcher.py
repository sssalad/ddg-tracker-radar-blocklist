import pandas
from domainDataFrame import DomainDataFrame

# Class to search DomainDataFrames. 
# Currently only searches categories, future search functions always need to return a dataframe so they can easily be chained together
class Searcher:
    def __init__(self, csvFile):
        self.df = pandas.read_csv(csvFile)

    def searchCategory(self, category, exclusionList):
        newDF = DomainDataFrame()

        # For each row...
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