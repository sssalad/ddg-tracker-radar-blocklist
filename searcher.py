import pandas
from domainDataFrame import DomainDataFrame

class Searcher:
    def __init__(self, csvFile):
        self.df = pandas.read_csv(csvFile)

    def searchCategory(self, category):
        newDF = DomainDataFrame()

        for index, row in self.df.iterrows():
            if category in row['categories']:
                input = [row['domain'], row['owner'], row['prevalence'], row['fingerprinting'], 
                                   row['cookies'], row['categories'], row['cnames']]
                newDF.appendDomain(input)

        return newDF.df