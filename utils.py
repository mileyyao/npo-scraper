from urllib.parse import urlsplit

# gets a list of the urls to crawl initially
# -- are prepended to links to ignore
def get_urls(filename='partner_urls.txt') -> list:
    urls = []
    for url in _read_file(filename):
        if '--' == url[:2]:
            print(f'Ignoring {url}')
            continue
        if 'http' not in url:
            urls.append(f'http://{url}')
        else:
            urls.append(url)
    return urls

# gets a list of the partner keywords
def get_kws(filename='partner_kw.txt'):
    return _read_file(filename)

# reads in filename as read only, returns list of stripped strings from file
def _read_file(filename):
    with open(filename, 'r') as file:
        return [kw.strip() for kw in file.readlines()]

# check to see if any of the partner words are in URL
def partner_match(url, logger=None):

    if not url: return False

    # the elegant solution is this
    if not logger:
        return any(kw in url for kw in get_kws())

    # but for logging purposes we will be verbose
    kws = get_kws()
    for kw in kws:
        if kw in url:
            logger.info(f'✅ {kw} was found in {url}.')
            return True

# check to see if any of the stop words are in URL
def stop_word_match(url, logger=None):

    if not url: return False

    # the elegant solution is this
    if not logger:
        return any(kw in url for kw in get_kws('stop_kw.txt'))

    # but for logging purposes we will be verbose
    kws = get_kws('stop_kw.txt')
    for kw in kws:
        if kw in url:
            logger.info(f'🛑 {kw} was encountered in {url}.')
            return True


# check to make sure we have a partner match and no stop words
def valid_partner_url(url, logger=None):
    return partner_match(url, logger) and not stop_word_match(url, logger)

# extracts the hostname of a given website
# i.e. stackoverflow.com/questions/12345 -> www.stackoverflow.com
def get_hostname(url):
    hostname =  urlsplit(url).hostname

    # already in good form
    if not hostname:
        return url

    if 'www' not in hostname:
        return f'www.{hostname}'
    return hostname

# validates a given url to ensure it is a valid partner
# base is the hostname of the site where the partner was found i.e. foodpantry.org
# url is the name of the partner site link i.e. soupkitchen.org (which was found in base)
# ensures no stop words are in the partner link (no fb, ig, twitter, yt, etc..)
def valid_partner(base, url, logger=None):



    return (get_hostname(base) != get_hostname(url) and
            not stop_word_match(url, logger) and
            'tel' not in url and
            'jpg' not in url)
