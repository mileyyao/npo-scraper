from scrapy import signals

import datetime
import scrapy
import utils
import json
import time
import os

timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%-m-%-d %H-%M-%S')
debug_path = os.path.join('debug', timestamp)

os.makedirs(debug_path)

out_file = os.path.join(debug_path, 'output.json')
log_file = os.path.join(debug_path, 'log.txt')
generated_urls = os.path.join(debug_path, 'urls.txt')

data = {}

start = time.time()

# clear out files
with open(out_file, 'w') as a, open(log_file, 'w') as b:
    pass

# debug purposes, simple health checks
def _health_check():
    with open(generated_urls, 'r') as urls, open(out_file, 'r') as output:

        no_urls = len(urls.readlines())
        no_keys = len(json.load(output).keys())

        # checks to see if number of base urls matches in read urls
        if no_urls == no_keys:
            print(f'✅ URL count validation pass: read: {no_urls} stored: {no_keys}')
        else:
            print(f'🚫 Health check fail. Number of URLs read in [{no_urls}] is not the same as output [{no_keys}].')


class OrgCrawler(scrapy.Spider):

    name = 'orgcrawler'

    custom_settings = {
        #'DOWNLOAD_TIMEOUT': 5
        'LOG_FILE': log_file
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
        urls = utils.get_urls(filename='partner_urls.txt')

        # debug purposes
        with open(generated_urls, 'w') as f:
            for url in urls:
                f.write(f'{url}\n')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_url)

    # called when spider is closed
    def spider_closed(self):
        with open(out_file, 'w') as f:
            f.write(json.dumps(data, indent=4))

        _health_check()

        self.logger.info(f'Total time elapsed: {datetime.timedelta(seconds=time.time() - start)}')
        print(f'Total time elapsed: {datetime.timedelta(seconds=time.time() - start)}')

    # crawling logic
    def parse_url(self, response):

        base = utils.get_hostname(response.url)

        # may want to add stop words for domains for bad redirects
        if 'dnsrsearch' in base:
            return
        if not base in data:
            data[base] = {
                'breadcrumbs': [],
                'partners': []
            }

        # TODO: create xpath string generator this should really be
        # TODO: '//a[not(contains(@href, "youtube")) and not(contains(@href, "facebook"))]'
        # TODO: because the facebook, twitter, etc links are still being crawled just not visited
        # anything on page that matches <a> tags
        for link in response.xpath('//a'):

            # get the link name, get the link url
            link_url = link.xpath('@href').get()
            full_url = response.urljoin(link_url)

            # on the right path - keep going
            if utils.valid_partner_url(link_url, self.logger) and full_url not in data[base]['breadcrumbs']:
                # Make sure we are still in domain (don't leave site)
                if utils.get_hostname(response.url) == utils.get_hostname(full_url):
                    data[base]['breadcrumbs'].append(full_url)
                    yield scrapy.Request(full_url, callback=self.parse_url)

            # not a partner match, but came from  a partner page i.e mysite/partners -> mysite.org
            elif utils.valid_partner_url(response.url):

                # get base name of partner
                partner_name = utils.get_hostname(full_url)

                # if the partner link is not in the list and make sure host names are not the same
                if partner_name not in data[base]['partners'] and utils.valid_partner(base, full_url, self.logger):
                    data[base]['partners'].append(partner_name)


                yield scrapy.Request(full_url, callback=self.scrape_url, meta={'base': base})

    # this function contain the main logic for scraping partner data off of a candidate page
    # TODO: Pages are only scraped once per session regardless of the source. Need to create additional
    # TODO: mapping for all parner information
    def scrape_url(self, response):

        # get the site we came from
        base = response.meta.get('base')