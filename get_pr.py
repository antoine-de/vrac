from dateutil import parser
from requests.auth import HTTPBasicAuth

__author__ = 'antoine'

import requests

github_api = 'https://api.github.com/repos/CanalTP/navitia'

def get_date_of_tag(tag):
    #not the github tag api do not provide name args, so we need to get all and filter
    github_all_tag_query = "{api}/tags".format(api=github_api)
    github_tag_response = requests.get(github_all_tag_query, auth=HTTPBasicAuth('give_yours', ''))

    if github_tag_response.status_code != 200:
        print github_tag_response
        print "impossible to find tag {} date".format(tag)
        return None

    tags = github_tag_response.json()
    print tags
    tag_dict = next(t for t in tags if t['name'] == tag)
    if not tag_dict:
        print "impossible to find tag {}".format(tag)
        return None

    commit_sha = tag_dict['commit']['sha']

    github_commit_response = requests.get("{api}/commits/{sha}".format(api=github_api, sha=commit_sha))
    if github_commit_response.status_code != 200:
        print "impossible to find commit {} ".format(commit_sha)
        return None

    date = github_commit_response.json()['commit']['committer']['date']
    return parser.parse(date, dayfirst=False, yearfirst=True)



#we get all closed PR since latest tag
#WARNING: it is not the list of merged PR since github does not have that
query = "{api}/pulls?state=closed&per_page=100".format(api=github_api)


print "query github api: " + query

github_response = requests.get(query, auth=HTTPBasicAuth('give_yours', ''))

if github_response.status_code != 200:
    message = github_response.json()['message']
    print "c'est la merde"
    exit(1)

closed_pr = github_response.json()

tag_date = get_date_of_tag('v1.18.2')

print "tag ============== {}".format(tag_date)

lines = []
for pr in closed_pr:
    merged_date_str = pr['merged_at']
    if merged_date_str is None:
        continue

    merged_date = parser.parse(merged_date_str, dayfirst=False, yearfirst=True)

    if merged_date < tag_date:
        print "c'est po bon, on en veut po, {} ===  de {}".format(merged_date, pr)
        continue


    #TODO use the date to filter with respect to the last tag time
    title = pr['title']
    url = pr['html_url']
    lines.append(u'  * {title}  <{url}>'.format(title=title, url=url))

for l in lines:
    print l