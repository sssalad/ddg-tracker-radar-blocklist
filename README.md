# ddg-tracker-radar-blocklist
These lists are generated an maintained using data from [DuckDuckGo's Tracker Radar](https://github.com/duckduckgo/tracker-radar). Lists are intended to be used by a [Pi-hole](https://pi-hole.net/).

Lists can be used directly from this Github in a Pi-hole instance, or this can be ran on a scheduled task to customize and save lists locally. Currently, lists are split up based on the [Tracker Radar categories](https://github.com/duckduckgo/tracker-radar/blob/main/docs/CATEGORIES.md) (Badge and CDN are excluded by default). 

# Installation 
### Prerequisits
* [Python 3.13.1 or later](https://www.python.org/downloads/)

### Download or Clone this Repository
```
git clone https://github.com/sssalad/ddg-tracker-radar-blocklist.git
```

### Install Required Python Libraries
```
cd ddg-tracker-radar-blocklist
pip install -r requirements.txt
```

### Run
```
python ddg-tr.py
```