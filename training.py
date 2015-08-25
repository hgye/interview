# -*- coding: utf-8 -*-

# !/usr/bin/env python

from collections import Counter
from collections import defaultdict
import os
import re
import operator
import json
import nltk
import pdb


class dataSet(object):

    def __init__(self, folder):
        # training_folder = ('training-data')
        # training_files = []
        # training_files += [each foreach in os.listdir(training_folder)
        #                    if each.endswith('.json')]

        # use nltk to tokenizer, model punkt etc.
        nltk.data.path.append('./nltk_data')
        self.JsonFolder = folder
        self.files = []
        self.files += [each for each in os.listdir(folder)
                       if each.endswith('.json')]

        # data is corpus from description
        # self.data = []

        # class_list is project name
        self.class_list = []

        # training set
        self.wordSet = defaultdict(list)
        self.wordFreqdata = []

    def processData(self):
        # corpus is raw from json file
        corpus = self.openJsonFile()

        issue_li = corpus[0]["issues"]
        field_li = [i["fields"] for i in issue_li]

        for d in field_li:
            proj = d["project"]["key"]
            desc = d["description"]

            if desc:
                self.appendWordSet(proj, desc)

        pdb.set_trace()
        self.genWordFreqData()

    def openJsonFile(self):
        data = []

        for each in self.files:
            # pdb.set_trace()
            each_file = self.JsonFolder + '/' + each
            with open(each_file, 'r') as f:
                data.append(json.load(f))

        return data

    def appendWordSet(self, proj, desc):
        tokens = nltk.word_tokenize(desc)
        text = nltk.Text(tokens)

        # remove punctuation, count raw words
        nonPunct = re.compile('.*[A-Za-z].*')
        hexNum = re.compile('0x.*')
        raw_words = [w for w in text if nonPunct.match(w)
                     if not hexNum.match(w)]

        # find proj in class_list
        if proj in self.class_list:
            pass
        else:
            self.class_list.append(proj)

        for p in self.class_list:
            self.wordSet[p] += raw_words

    def genWordFreqData(self):
        for t in self.wordSet.items():
            raw_word_count = Counter(t[1])

            # result is list, pairs within [(word, freq)]
            results = sorted(
                raw_word_count.items(),
                key=operator.itemgetter(1),
                reverse=True)

            self.wordFreqdata.append((t[0], results))

    def getWordFreqData(self):
        return self.wordFreqdata

training = dataSet('./training-data')
training.processData()
train_data = training.getWordFreqData()

f = open('word.txt', 'w+')
f.truncate()
for i in train_data:
    f.write(i[0])
    f.write("\n")
    for item in i[1][:100]:
        f.write(u"{}\t".format(item))
    f.write("\n")
f.close()
