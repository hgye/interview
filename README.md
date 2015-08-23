# Interview Homework

---

### Introduction
This paper applies for new Python user but familiar with one or more other programming languages as well as having a solid experience on modularized software development.

The candidates are expected to demonstrate a fast learning skill to master python development environment setup in less than 6 hours working time and the ability to grasp correct utilization of [nltk](http://www.nltk.org/) Python library.  

### Problem Statement
* In telecommunication industry, automation is more and more important even vital to the success of fast response and iterative delivery. Furthermore, when a big number of software candidate issues are reported, the techniques of automatic sorting is still not well defined over this industry. 
* The candidates are expected to design a program which utilizes appropriate Python libraries to train a classifier with given "[training data](https://github.com/goteststar/interview/tree/master/training-data)" and generate results on "[test data](https://github.com/goteststar/interview/tree/master/test-data)". After that the candidates can calculate the accuracy and prepare a description on how to improve it.
* During the training step, key `training-data[0]["issues"]['fields']['project']['key']` is regarded as catalog title and the features (word list) should be extracted from `training-data[0]['fields']['description']]`. In other words, the candidate should training classifier with given project names (as "TONTC", "PREM") and description section (a word list in JSON).  
* During the test action,
* Candidates can upload codes to their own repo on [github](https://github.com/), [gitcafe](https://gitcafe.com/), [bitbuckets](https://bitbucket.org/).
*  Alternatively, if candidate is more familiar with IPython, it is appreciated if s/he would send back the IPython-NB format file in email or share the link.


### JSON Data description
*  [Training data](https://raw.githubusercontent.com/goteststar/interview/master/training-data/group-ppl-0822-orig.json) and test data have the same format in this paper.
*  Training data JSON format:
   
`   data[0]['total'] # the total number of issue records in this JSON object`
`	data[0]["issues"] # the list of issues in this JSON object`
`   data[0]["issues"][i]['fields']['project']['key'] # the project name for given issue record`
`	data[0]["issues"][i]['fields']['summary'] # The given word list to feed to classifier`

Below is the data structure. Here the author only list the data to process and ignore the other columns.

JSON

|total|issues|
|---|---|
|220|**list**|

issues

|fields|
|---|
|**list**|

fields

|description|project|
|---|---|
|<font color="blue">The text list to process<font>|**list**|

project: `['key']` is the project name as catalog title. 

|key|
|---|
|<font color="blue">TONTC<font>|

### Notes
* Candidates are expected to describe what happened to below operation on Linux or Cygwin(Linux environment simulator) to get a warm-up on this problem first.

> [mawu.NANL-MAWU] ➤ curl -D- -b ../cookies/cache-2015-0822.maxwu  -X POST -H "Content-Type: application/json" --data  '{ "jql":"reporter in (zhangsan, lisi, wangwu, maliu) AND created >= 2015-08-15 AND created <2015-08-22 AND type = Bug","maxResults":10000,"fields":["id","key"]}' "http://jira.calix.local/rest/api/2/search"  |grep '"total":[0-9]*' -o |tr ":" " " |awk '{print "Total"=$2,($2>=15)? "Yes": "No" }'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  6997    0  6787  100   210   5414    167  0:00:01  0:00:01 --:--:--  5455
42 Yes

[2015-08-23 12:44.25]  ~/devel/GoJira/4interview
[mawu.NANL-MAWU] ➤

* Given a small training set, the accurancy is expected to be higher than 60%.
* Candidates can directly pick up default algorithm in nltk or any other official Python package on PyPi service.
* Candidates shall prepare to present the logics and improvement points.
* Candidates shall consider if this technique can be applied to test case selection while planning test project w/in shared source code branches to different HW module products.
* It would be an advantage if candidate can compare multiple algorithm.
