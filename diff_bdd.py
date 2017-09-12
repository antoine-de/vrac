import csv

before_file = '/tmp/before.csv'
after_file = '/tmp/after.csv'


before_dict = {}
with open(before_file) as f:
    reader = csv.reader(f, delimiter=';')
    # before_dict = {(l[0], l[1]): l for l in reader}
    for l in reader:
        # if before_dict.has_key((l[0], l[1])):
        #     print "duplicate key! {}".format(l)
        before_dict[(l[0], l[1])] = l
    print "{} before lines loaded".format(len(before_dict))

with open(after_file) as f:
    reader = csv.reader(f, delimiter=';')
    after_lines = reader

    output_path = '/tmp/not_in_before'
    with open(output_path, 'wb') as f:
        f.write('source_node_id;target_node_id;st_astext\n')

        for l in after_lines:
            before_obj = before_dict.get((l[0], l[1]))
            if before_obj:
                pass
                # if before_obj != l:
                #     print "strange, the geometry are not equals: old = {}, new = {}".format(before_obj, l)
            else:
                f.write(';'.join(l) + '\n')
