from itertools import izip
import re

file_name='sources_sorted.list'

with open(file_name) as f:
    lines = f.readlines()

good_lines = []
for l in lines:
    good_lines.append(l.replace('\n',''))

tuples = []
for i in range(0, len(good_lines), 2):
    tuples.append((good_lines[i], good_lines[i+1]))

def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)

with open("instances") as f:
    instances = f.readlines()

done = set()

for i in instances:
    found = False
    for instance_name, source_dir in tuples:
        if '"{}"'.format(instance_name) in i:
            print re.sub("\)$\n", ", source_dir='{}')".format(source_dir), i)
            found = True
            break
    if not found:
        print i


#for instance_name, source_dir in pairwise(good_lines):
#    if instance_name in done:
#        continue
#    found = False
#    for i in instances:
#        if instance_name in done:
#            continue
#        if instance_name in i:
#            print re.sub("\)$\n", ", source_dir='{}')".format(source_dir), i)
#            done.add(instance_name)
#            found = True
#
#    if not found:
#        for i in instances:
#            if instance_name in i:





