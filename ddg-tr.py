import json
from domainDataFrame import DomainDataFrame

#input = '/home/ssalad/Documents/ddg-tracker-radar-blocklist/domains/NO/0i0i0i0.com.json'
input = 'https://raw.githubusercontent.com/duckduckgo/tracker-radar/refs/heads/main/domains/NO/0i0i0i0.com.json'

with open(input, mode='r', encoding="utf-8") as read_file:
    data = json.load(read_file)
'''
self.df = pandas.DataFrame(columns=['domain', 'owner', 'prevalence', 
                                    'fingerprinting', 'cookies', 
                                    'categories', 
                                    'cnames'])
'''

df = DomainDataFrame()
input = [data['domain'], data['owner'], data['prevalence'], data['fingerprinting'],
         data['cookies'], data['categories'], data['cnames']]
df.appendDomain(input)
print(df.df)
