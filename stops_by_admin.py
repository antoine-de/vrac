#encoding utf-8
# To run this you need to install navitia_wrapper
# pip install -e "git+https://github.com//CanalTP/navitia_python_wrapper#egg=navitia_wrapper"
# pip install requests

from collections import defaultdict
import navitia_wrapper
import logging
import csv

logging.basicConfig(level=logging.DEBUG)

NAVITIA_URL = 'https://api.navitia.io/'
NAVITIA_TOKEN = 'give_yours'
NAVITIA_INSTANCE = 'fr-pdl'
partenaire = 'C53'

def make_navitia_wrapper():
    """
    return a navitia wrapper to call the navitia API
    """
    url = NAVITIA_URL
    token = NAVITIA_TOKEN
    instance = NAVITIA_INSTANCE
    return navitia_wrapper.Navitia(url=url, token=token).instance(instance)


navitia_wrapper = make_navitia_wrapper()

stops_areas = navitia_wrapper._whole_collection('contributors/{partenaire}/stop_areas'.format(partenaire=partenaire))

admins_by_stops = defaultdict(list)
for s in stops_areas:
    stop_id = s.get('id')
    stop_name = s.get('name')

    admins = s.get('administrative_regions')

    if len(admins) > 1:
        logging.debug('we have {} admins for the stop_area {}'.format(len(admins), stop_id))

    for a in admins:
        admins_by_stops[(a.get('id'), a.get('name'))].append(s)


with open('admin_by_stops.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['admin_id', 'admin_name', 'stop_id', 'stop_name'])
    for admin, stops in admins_by_stops.items():
        for s in stops:
            writer.writerow([admin[0], admin[1], s.get('id'), s.get('name')])
