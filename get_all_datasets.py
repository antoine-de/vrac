import requests

cov_url = 'https://api.navitia.io/v1/coverage'
auth = ('give_yours', '')

all_coverages = requests.get(cov_url, auth=auth)

all_coverages_id = [c['id'] for c in all_coverages.json()['regions']]

total_datasets = 0
for c in all_coverages_id:

    all_coverages = requests.get('{cov}/{id}/datasets'.format(cov=cov_url, id=c), auth=auth)


    nb_datasets = all_coverages.json().get('pagination', {}).get('total_result', 0)

    print 'coverage {}, datasets {}'.format(c, nb_datasets)
    total_datasets += nb_datasets


print 'total datasets = {}'.format(total_datasets)
