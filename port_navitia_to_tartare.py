import json
import requests
from clingon import clingon


def get_navitia_instances(url, token):
    raw = requests.get('{nav}/v1/coverage'.format(nav=url), auth=(token, ''))

    json = raw.json()

    print('json = {}'.format(json))
    return [c['id'] for c in json.get('regions', [])]


def create_tartare_instances(instances, tartare_url, env):
    print('instances = {}'.format(instances))

    print('posting to tartare')
    for i in instances:
        id = i
        name = i.split('-')[-1]  # heuristic to get a name out of the id

        args = {
            'id': id,
            'name': name,
            'input_dir': '/var/tartare/input/{instance_up}/{env}/FUSIO/EXPORT'.format(instance_up=i.to_upper(),
                                                                                env=env.to_upper())
        }
        resp = requests.post('{tartare}/coverages'.format(tartare=tartare_url),
                             headers={'Content-Type': 'application/json'},
                             data=json.dumps(args))

        if resp.status_code != 201:
            print('error while posting to tartare : {}'.format(resp.text))
        else:
            print('post {} ok'.format(i))


def update_tartare_instances(instances, tartare_url, env):
    print('updating tartare')
    for i in instances:
        args = {
            'input_dir': '/var/tartare/input/{instance_up}/{env}/FUSIO/EXPORT'.format(instance_up=i.upper(),
                                                                                env=env.upper())
        }
        resp = requests.patch('{tartare}/coverages/{id}'.format(tartare=tartare_url, id=i),
                             headers={'Content-Type': 'application/json'},
                             data=json.dumps(args))

        if resp.status_code != 200:
            print('error while patching tartare : {}'.format(resp.text))
        else:
            print('post {} ok'.format(i))

@clingon.clize()
def create_all_coverages(nav_url='',
                         nav_token='',
                         tartare_url='',
                         env=''):
    instances = get_navitia_instances(nav_url, nav_token)

    update_tartare_instances(instances, tartare_url, env)
    # create_tartare_instances(instances, tartare_url, env)