import pandas

# Simple class for maintaining a pandas dataframe for the domains. Mostly useful to define the appendDomain function
class DomainDataFrame:
    def __init__(self):
        self.df = pandas.DataFrame(columns=['domain', 'owner', 'prevalence', 'fingerprinting', 'cookies', 'categories', 'cnames'])

    def appendDomain(self, domainList):
        self.df = pandas.concat([pandas.DataFrame([domainList], columns=self.df.columns), self.df], ignore_index=True)