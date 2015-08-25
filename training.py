# -*- coding: utf-8 -*-

# !/usr/bin/env python

from collections import Counter
from collections import defaultdict
import os
import re
import operator
import json
import nltk
# import pdb

training_folder = ('training-data')
training_files = []
training_files += [each for each in os.listdir(training_folder)
                   if each.endswith('.json')]

# data is corpus from description
data = []

# class_list is project name
class_list = []

# training set
train_set = defaultdict(list)
train_data = []

for each in training_files:
    # pdb.set_trace()
    each_file = training_folder + '/' + each
    with open(each_file, 'r') as f:
        data.append(json.load(f))


issue_li = data[0]["issues"]
field_li = [i["fields"] for i in issue_li]

# f = open("desc.txt", 'a+')
# f.truncate()

# for d in field_li:
#     key = d["project"]["key"]
#     desc = d["description"]
#     f.write("***********\n".encode('utf-8'))
#     f.write("project key is:".encode('utf-8'))
#     f.write(key.encode('utf-8'))
#     f.write("\n")
#     f.write(desc.encode('utf-8'))
#     f.write("\n")

# f.close()

for d in field_li:
    proj = d["project"]["key"]
    desc = d["description"]

    if desc:

        # use nltk to tokenizer, model punkt etc.
        nltk.data.path.append('./nltk_data')
        tokens = nltk.word_tokenize(desc)
        text = nltk.Text(tokens)

        # remove punctuation, count raw words
        nonPunct = re.compile('.*[A-Za-z].*')
        hexNum = re.compile('0x.*')
        raw_words = [w for w in text if nonPunct.match(w)
                     if not hexNum.match(w)]
#        pdb.set_trace()
        # find proj in class_list
        if proj in class_list:
            pass
        else:
            class_list.append(proj)

        for p in class_list:
            train_set[p] += raw_words


for t in train_set.items():
    raw_word_count = Counter(t[1])

    # result is list, pairs within [(word, freq)]
    results = sorted(
        raw_word_count.items(),
        key=operator.itemgetter(1),
        reverse=True)

    train_data.append((t[0], results))


f = open('word.txt', 'w+')
f.truncate()
for i in train_data:
    f.write(i[0])
    f.write("\n")
    for item in i[1][:100]:
        f.write(u"{}\t".format(item))
    f.write("\n")
#   f.write(i[0])
#    f.write[i[1]]
f.close()
