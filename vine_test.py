from __future__ import print_function
from vine import promise, barrier
import requests
from concurrent import futures

def get(*url):
    print('url')
    print(url)
    with futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(requests.get, url[0])
        return future.result().status_code

def all_done():
    print("s")

    pass  # all requests complete

p1 = promise()
p1.then(promise(print, ('OK',))).then(promise(get, ('http://sina.com',))).then(promise(get, ('http://navitia.io',)))
#p1()

p2 = promise()
p2.then(promise(print, ('OK',))).then(promise(get, ('http://sina.com',))).then(promise(get, ('http://navitia.io',)))


a = barrier([p1, p2], callback=all_done)
a.finalize()
a('a')
a('a')
a('a')


