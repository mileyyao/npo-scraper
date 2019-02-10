
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

    # return [f'http://{file}' if 'http' not in file else file for file in _read_file(filename)]

# gets a list of the partner keywords
def get_kws(filename='partner_kw.txt'):
    return _read_file(filename)

# reads in filename as read only, returns list of stripped strings from file
def _read_file(filename):
    with open(filename, 'r') as file:
        return [kw.strip() for kw in file.readlines()]

# check if a list of strings (kws) is a substring of kw
def check_kw(kw, logger=None):

    # get keywords, stop_words
    kws = get_kws()
    stop = get_kws(filename='stop_kw.txt')

    # empty link
    if not kw: return False

    # the elegant solution is
    # make sure the link has a keyword and not a stop word in it
    if not logger:
        return any(k in kw for k in kws) and not any(k in kw for k in stop)

    # but for logging purposes we will be verbose

    # make sure there is no stop word in URL
    for stop_word in stop:
        if stop_word in kw:
            logger.info(f'>> Found {stop_word} in url: {kw}')
            return False

    # check to see if there is a keyword in URL
    for keyword in kws:
        if keyword in kw:
            logger.info(f'>> Found {keyword} in url: {kw}')
            return True

    # no stop word, but no keyword, no good
    logger.info(f'>>No keyword found in url: {kw}')
    return False