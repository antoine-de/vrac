from itertools import izip
import re

log_dir = '/home/antoine/run/navitia/bench/jmeter'
file_name = 'kraken_log_v1.14_optim_time_and_response'

file_path = log_dir + '/' + file_name

with open(file_path) as f:
    lines = f.readlines()

good_lines = []
for l in lines:
    good_lines.append(l.replace('\n',''))

tuples = []
for i in range(0, len(good_lines)-2, 3):
    nb_sol_match = re.match('.*found ([0-9]+).*', good_lines[i])
    if nb_sol_match:
        nb_sol = nb_sol_match.group(1)
    else:
        nb_sol = None
    time_match = re.match('.*processing time : ([0-9]+) .*', good_lines[i+1])
    if time_match:
        time = time_match.group(1)
    else:
        time = None
    tuples.append((nb_sol, time))

output_path = log_dir + '/' + file_name + '_gen.csv'
cpt = 0
with open(output_path, 'wb') as f:
    f.write('idx;nb_sol; time\n')
    for t in tuples:
        cpt += 1
        f.write("{};{};{}\n".format(cpt, t[0], t[1]))

print tuples
