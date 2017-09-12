import requests

url = 'https://api.navitia.io/v1/coverage/sncf/trips'

page = 0
while True:
    print 'callling page {}'.format(page)
    res = requests.get(url, params={'count': 100, 'start_page': page},
                       auth=('2c0446e8-f206-4500-a82b-10d28d7cdd33', ''))
    if res.status_code != 200:
        print 'probleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeem : page : {}'.format(page)
        break

    js = res.json()

    if js.get('error'):
        print 'probleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeem : erreur: {}'.format(js)
        break

    if not js.get('trips', []):
        print 'arret a la page {}'.format(page)
        break

    for trip in js['trips']:
        vj = requests.get(url + '/' + trip['id'] + '/vehicle_journeys',
                       auth=('give_yours', ''))

        if vj.status_code != 200:
            print 'pb trip {}'.format(trip)
            raise ValueError('trip {} mauvais'.format(trip['id']))

    page += 1