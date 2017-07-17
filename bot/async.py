from __future__ import print_function
import sys

urls = ['http://www.google.com', 'http://www.yandex.ru', 'http://www.python.org']

import gevent
from gevent import monkey

# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()


if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib2 import urlopen


def print_head(url):
    print('Starting %s' % url)
    data = urlopen(url).read()
    return len(data)
   # print('%s: %s bytes: %r' % (url, len(data), data[:50]))

jobs = [gevent.spawn(print_head, url) for url in urls]
gevent.wait(jobs)
print([job.value for job in jobs])