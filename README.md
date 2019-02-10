## NPO Partner Web Scraper

To execute the program, run the command  
```scrapy runspider main.py --logfile=log.txt```

This program attempts to find all possible partner non-profit organizations given a set of "seed URLs".
These URLs will serve as input for the program.

The program will attempt to traverse all possible links on a page that match our criteria.

Initial development utilizes [scrapy](https://scrapy.org) as the main crawling engine.

Output is currently in JSON format, with hopes to expose an API that will return neighbors for a 
set of URLs.  

**Current state**: JSON output contains a list of keys corresponding to the hostname of the websites
provided in the seed list. The value is another dictionary whose values represent "breadcrumbs" and 
partners. Breadcrumbs are a list of links on how the scraper got to the partner page. Partners are
potential matches.

```json
{
    "www.ccrcda.org": {
        "breadcrumbs": [
            "http://www.ccrcda.org/agencies_and_programs/",
            "http://www.ccrcda.org/agencies_and_programs/Catholic-Charities-Tri-County-Services_109_13_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Saratoga-Warren-Washington-Counties_109_2_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Catholic-Charities-of-Columbia-and-Greene-Counties_109_3_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Catholic-Charities-of-Herkimer-County_109_4_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Catholic-Charities-of-Delaware-Otsego-Schoharie_109_5_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Catholic-Charities-of-Fulton-Montgomery-Counties_109_6_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Care-Coordination-Services_110_7_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Catholic-Charities-Disabilities-Services_110_8_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Senior-Caregiver-Support-Services_110_9_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Community-Maternity-Services_110_10_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Catholic-Charities-Housing-Office_110_11_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/United-Tenants-of-Albany_110_12_sb.htm",
            "http://www.ccrcda.org/agencies_and_programs/Additional-Programs_111_pg.htm",
            "http://www.ccrcda.org/agencies_and_programs/2016-Migrant-Crisis_125_pg.htm"
        ],
        "partners": [
            "https://www.spiraldesign.com/",
            "http://www.cchoalbany.org",
            "http://www.depaulhousing.com",
            "https://www.ccseniorservices.org/",
            "http://www.ccherkimercounty.org/",
            "https://www.catholiccharitiescg.org"
        ]
    }
}
```

**Note:** You may want to adjust the ``DOWNLOAD_TIMEOUT`` setting in ``main.py``. It is currently set to
5 seconds (default is 180) for quicker debugging.

You can prepend ``--`` to any line in the partner_urls.txt file to exclude it from being read in.

``main.py`` - crawling logic  
``utils.py`` - data cleaning and utilities  
``partner_kw.txt`` - keywords to grab partner data  
``stop_kw.txt`` - stop words  
``partner_urls.txt`` - seed URLs  
``slim_urls.txt`` - test/debug URLs  
``output.json`` - JSON object representation relations between partners and base sites  
``log.txt`` - scrapy log. also include s traces of URLs and which keywords/stop words were used to traverse.