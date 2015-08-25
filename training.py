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


class trainDataSet(object):

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
        self.trainSet = defaultdict(list)
        self.word_features = []
        self.trainData = []

    def processData(self):
        # corpus is raw from json file
        data = self.openJsonFile()

        issue_li = data[0]["issues"]
        field_li = [i["fields"] for i in issue_li]

        corpus = []
        for d in field_li:
            proj = d["project"]["key"]
            desc = d['description']
            if desc:
                self.addToCorpusAndGenDocument(proj, desc, corpus)

        # get all word, now it's time to get all word
        all_words = nltk.FreqDist(w for w in corpus)
        self.word_features = all_words.keys()[:2000]

        # featureList = []

        # for (proj, desc) in self.trainSet:
        #    feature = self.document_features(desc, word_features)
        #    featureList.append(feature)

        # then we decide document feature
        self.trainData = [(self.document_features(d), c)
                          for (c, d) in self.trainSet.items()]

    def openJsonFile(self):
        data = []

        for each in self.files:
            # pdb.set_trace()
            each_file = self.JsonFolder + '/' + each
            with open(each_file, 'r') as f:
                data.append(json.load(f))

        return data

    def addToCorpusAndGenDocument(self, proj, desc, corpus):
        tokens = nltk.word_tokenize(desc)
        text = nltk.Text(tokens)

        # remove punctuation, count raw words
        nonPunct = re.compile('.*[A-Za-z].*')
        hexNum = re.compile('0x.*')
        raw_words = [w for w in text if nonPunct.match(w)
                     if not hexNum.match(w)]

        corpus += raw_words

        # find proj in class_list
        if proj in self.class_list:
            pass
        else:
            self.class_list.append(proj)

        for p in self.class_list:
            self.trainSet[p] += raw_words

    def document_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features
    # def appendWordSet(self, proj, desc):
    #     tokens = nltk.word_tokenize(desc)
    #     text = nltk.Text(tokens)

    #     # remove punctuation, count raw words
    #     nonPunct = re.compile('.*[A-Za-z].*')
    #     hexNum = re.compile('0x.*')
    #     raw_words = [w for w in text if nonPunct.match(w)
    #                  if not hexNum.match(w)]

    #     # find proj in class_list
    #     if proj in self.class_list:
    #         pass
    #     else:
    #         self.class_list.append(proj)

    #     for p in self.class_list:
    #         self.trainSet[p] += raw_words

    # def genWordFreqData(self):
    #     for t in self.trainSet.items():
    #         raw_word_count = Counter(t[1])

    #         # result is list, pairs within [(word, freq)]
    #         results = sorted(
    #             raw_word_count.items(),
    #             key=operator.itemgetter(1),
    #             reverse=True)

    #         self.wordFreqdata.append((t[0], results))

    def getTrainData(self):
        return self.trainData

# training = trainDataSet('./training-data')
# training.processData()
# trainSample = training.getTrainData()

# for i in trainSample:
# pdb.set_trace()

class TextClassification(object):

    def __int__(self):
        self.trainData = []
        self.testData = []

    def fillSmaple(self, trainFolder='./training-data',
                   testFolder='./test-data'):

        training = trainDataSet(trainFolder)
        training.processData()
        self.trainData = training.getTrainData()

        testing = trainDataSet(testFolder)
        testing.processData()
        self.testData = testing.getTrainData()

    def classification(self):

        print "train number:", len(self.trainData)
        print "\n test number:", len(self.testData)

        ## use NaiveBayesClassifie
        classifier = nltk.NaiveBayesClassifier.train(self.trainData)
        test_error = nltk.classify.accuracy(classifier, self.testData)
        print "test accuracy:", test_error
        return test_error

classifier = TextClassification()
classifier.fillSmaple()
classifier.classification()
