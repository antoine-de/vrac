
import csv
import os
import itertools
import random
import copy
import codecs

from uniseg.graphemecluster import grapheme_clusters

# generate fuzzy tests for autocomplete

file_path = '/home/antoine/dev/bin/osm-geocoding-tester/osm_geocoding_tester/world/france/iledefrance/'
fuzzy_test_file = os.path.join(file_path, 'test_addresses.csv')

generated_file = os.path.join(file_path, 'test_addresses_fuzzy.csv')


def get_fuzzy_string(s):
    words = query.split(' ')
    letters = [letter for c in words for letter in (c + ' ')]
    start = len(words[0]) + 1
    letter_to_delete = random.randint(start, len(letters) - 1)

    letters_to_delete = []
    while letter_to_delete <= len(letters) - 1:
        letters_to_delete.append(letter_to_delete)
        if ord(letters[letter_to_delete]) <= 128:
            break
        letter_to_delete += 1

    print "size: {} delete [{}-{}]".format(len(letters), letters_to_delete[0], letters_to_delete[-1])
    modified_query = letters[0:letters_to_delete[0] - 1] + (letters[letters_to_delete[-1]:] if letters_to_delete[-1] < len(letters) else [])

    return modified_query


def get_grapheme_fuzzy_string(s):
    words = query.split(' ')
    all_but_first = ' '.join(words[- len(words) + 1:])

    cluster = list(grapheme_clusters(all_but_first))

    grapheme_to_delete = random.randint(0, len(cluster) - 1)

    modified_query = words[0] + ' ' + ''.join(itertools.chain(cluster[0:grapheme_to_delete] + cluster[grapheme_to_delete + 1:]))

    print u"query  = {}, grapheme removed = {}, modified_query : {}".format(
        query, cluster[grapheme_to_delete], modified_query)

    return modified_query

lines = []
with open(fuzzy_test_file) as f:
    reader = csv.reader(f, delimiter=',')

    header = True
    for raw_l in reader:
        l = [w.decode('utf-8') for w in raw_l]
        if header:
            lines.append(l)
            header = False
            continue

        query = copy.deepcopy(l[0])

        modified_query = get_grapheme_fuzzy_string(query)

        # we randomly remove one letter in a word (but not the first one, it's the street number)
        modified_query_word = ''.join(modified_query)
        lines.append(list(itertools.chain([modified_query_word], l[-len(l) + 1:])))

with open(generated_file, 'wb') as f:
    for l in lines:
        for w in l:
            f.write(','.join([w.encode('utf-8') for w in l]) + '\n')