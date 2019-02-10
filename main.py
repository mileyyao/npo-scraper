from scrapy import signals

import datetime
import scrapy
import utils
import json
import time

out_file = 'output.json'
log_file = 'log.txt'

data = {}

start = time.time()

# clear out files
with open(out_file, 'w') as a, open(log_file, 'w') as b:
    pass


class OrgCrawler(scrapy.Spider):

    name = 'orgcrawler'

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 5
    }

    # called when the spider is closed, will be used for reporting purposes
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(OrgCrawler, cls).from_crawler(crawler, *args, **kwargs)

        # register closed method
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    # get urls, generate request objects to crawl
    # will call parse() to crawl
    def start_requests(self):
        urls = utils.get_urls(filename='slim_urls.txt')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_url)

    # called when spider is closed
    def spider_closed(self):
        with open(out_file, 'w') as f:
            f.write(json.dumps(data, indent=4))

        self.logger.info(f'Total time elapsed: {datetime.timedelta(seconds=time.time() - start)}')
        print(f'Total time elapsed: {datetime.timedelta(seconds=time.time() - start)}')

    # crawling logic
    def parse_url(self, response):

        base = utils.get_hostname(response.url)
        if not base in data:
            data[base] = {
                'breadcrumbs': [],
                'partners': []
            }

        # anything on homepage that matches <a> tags
        for link in response.xpath('//a'):

            # get the link name, get the link url
            link_url = link.xpath('@href').get()
            full_url = response.urljoin(link_url)

            # check to see if link matches keywords and make sure we haven't already recorded it
            # this "drills down" until we have found a candidate 'partner' page for the site
            if utils.check_kw(link_url, self.logger) and full_url not in data[base]['breadcrumbs']:
                data[base]['breadcrumbs'].append(full_url)
                yield scrapy.Request(full_url, callback=self.parse_url)

            # most/all of the partner sites will not have our partner keywords listed
            # i.e unitedway.com is not a keyword hit
            # so we check to see if we came from a keyword hit previously, and scrape the current page for partner data
            elif utils.check_kw(response.url):
                # print(f'Currently at {response.url}. Next link is {full_url}')
                yield scrapy.Request(full_url, callback=self.scrape_url, meta={'base': base})

    # this function contain the main logic for scraping partner data off of a candidate page
    def scrape_url(self, response):

        # get the site we came from
        base = response.meta.get('base')
        # if the partner link is not in the list and make sure host names are not the same
        if response.url not in data[base]['partners'] and utils.valid_partner(base, response.url):
            data[base]['partners'].append(response.url)
