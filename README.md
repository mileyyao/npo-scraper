## NPO Partner Web Scraper

This program attempts to find all possible partner non-profit organizations given a set of "seed URLs".
These URLs will serve as input for the program.

The program will attempt to traverse all possible links on a page that match our criteria.

Initial development utilizes [scrapy](https://scrapy.org) as the main crawling engine.

Output is currently in JSON format, with hopes to expose an API that will return neighbors for a 
set of URLs.  

**Current state**: Outputs rudimentary relations of possible partner links. 
No scraping of partner data has been done. JSON output contains many duplicates.

``main.py`` - crawling logic  
``utils.py`` - data cleaning and utilities  
``partner_kw.txt`` - keywords to grab partner data  
``stop_kw.txt`` - stop words  
``partner_urls.txt`` - seed URLs  
``slim_urls.txt`` - test/debug URLs  
``output.json`` - JSON object representation relations between partners and base sites  
``log.txt`` - scrapy log. also includes traces of URLs and which keywords/stop words were used to traverse.