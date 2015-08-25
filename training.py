# -*- coding: utf-8 -*-

# !/usr/bin/env python

# from collections import defaultdict
import os
import re
import json
import nltk
# import pdb


class rawDataSet(object):

    def __init__(self, folder):
        # use nltk to tokenizer, model punkt etc.
        nltk.data.path.append('./nltk_data')
        self.JsonFolder = folder
        self.files = []
        self.files += [each for each in os.listdir(folder)
                       if each.endswith('.json')]

        # class_list is project name
        self.class_list = []

        # training set
        # self.trainSet = defaultdict(list)
        self.rawData = []
        self.word_features = []

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

        self.rawData.append((proj, raw_words))

    def document_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    def getRawData(self):
        return self.rawData

    def getWordFeatures(self):
        return self.word_features


class ProjectClassification(object):

    def __int__(self):
        self.trainData = []
        self.testData = []
        self.word_features = []

    def fillSmaple(self, trainFolder='./training-data',
                   testFolder='./test-data'):

        training = rawDataSet(trainFolder)
        training.processData()
        self.word_features = training.getWordFeatures()
        self.trainData = [(self.document_features(d), c)
                          for (c, d) in training.getRawData()]

        # self.trainData = training.getTrainData()

        testing = rawDataSet(testFolder)
        testing.processData()
        self.testData = [(self.document_features(d), c)
                         for (c, d) in testing.getRawData()]

    def document_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    def classification(self):

        print "train number:", len(self.trainData)
        print "\n test number:", len(self.testData)

        # pdb.set_trace()
        # use NaiveBayesClassifie
        classifier = nltk.NaiveBayesClassifier.train(self.trainData)
        test_error = nltk.classify.accuracy(classifier, self.testData)
        print "test accuracy:", test_error
        return test_error

if __name__ == '__main__':
    classifier = ProjectClassification()
    classifier.fillSmaple()
    classifier.classification()
