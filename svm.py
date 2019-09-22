# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn import preprocessing
from sklearn import svm

listCsv = ['bothScored', 'over15', 'over25', 'over35', 'awayWins', 'homeWins',
       'drawResult', 'homeScores', 'awayScores', 'homeHT', 'awayHT', 'drawHT',
       'homePSF', 'awayPSF', 'drawPSF', 'over05HT', 'over15HT', 'over25HT',
       'under15', 'under25', 'under35', 'under05HT', 'under15HT', 'under25HT',
       '1X', 'X2', '12', 'HT1X', 'HTX2', 'HT12', 'awayHTScores','homeHTScores']

leagues = ['spain0', 'italy0', 'england0',
           'germany0', 'france0', 'portugal0', 'netherlands0']

errorYears = {'england0' : [2014], 'france0' : [2011, 2016],
              'germany0' : [], 'italy0' : [2012, 2014, 2015, 2016],
              'netherlands0' : [], 'portugal0' : [], 'spain0' : []}

startYears = {'england0' : 2004, 'france0' : 2007, 'germany0' : 2006,
              'italy0' : 2006, 'netherlands0' : 2017, 'portugal0' : 2017,
              'spain0' : 2005}


def getMatrices(function, country, league, year):
    country = country[:-1]
    path = os.getcwd()
    countryupp = country[0]
    countryupp = chr(ord(countryupp) - 32)
    gen_data_folder = country + '\\' + str(league) + '\\' + str(year) + '\\'
    filename = 'csv_' + function
    relPath = '\generated_data\\' + gen_data_folder + filename
    path = os.getcwd() + relPath
    no_params = 54
    print(no_params)
    print(path)
    names = []
    names.append('Result')
    for i in range(no_params):
        names.append(str(i + 1))
    data2 = pd.read_csv(path, header = None,
                names = names)
#    data2 = (data2 - data2.mean()) / data2.std()
    data2.insert(1, 'Ones', 1)
    ## set X and y (remember from above that we moved the label to column 0)
    cols = data2.shape[1]
    print(cols)
    X2 = data2.iloc[:,1:cols]
    y2 = data2.iloc[:,0:1]
    ## convert to numpy arrays and initalize the parameter array theta
    X2 = np.array(X2.values)
    y2 = np.array(y2.values)
    min_max_scaler = preprocessing.MinMaxScaler()
    X2 = min_max_scaler.fit_transform(X2)
    return X2, y2


def trainSvm(function):
    filename = 'csv_' + function
    no_params = 54
    names = []
    names.append('Result')
    for i in range(no_params):
        names.append(str(i + 1))
    data2 = pd.read_csv(filename, header = None,
                names = names)
#    data2 = (data2 - data2.mean()) / data2.std()
    data2.insert(1, 'Ones', 1)
    ## set X and y (remember from above that we moved the label to column 0)
    cols = data2.shape[1]
    print(cols)
    X2 = data2.iloc[:,1:cols]
    y2 = data2.iloc[:,0:1]
    ## convert to numpy arrays and initalize the parameter array theta
    X2 = np.array(X2.values)
    y2 = np.array(y2.values)
    min_max_scaler = preprocessing.MinMaxScaler()
    X2 = min_max_scaler.fit_transform(X2)
    svc = svm.SVC()
    svc.fit(X2, y2)
    print('Training accuracy = {0}%'.format(np.round(svc.score(X2, y2) * 100, 2)))
    return svc

def testOn(tested_func, svc):
    res = []            
    for country in leagues:
        league = int(country[-1])
        for year in range(startYears[country], 2019):
            if year not in errorYears[country]:
                X, y = getMatrices(tested_func, country, league, year)
                res.append(np.round(svc.score(X, y) * 100, 2))
    return res
            

#svc = trainSvm('bothScored')
#res = testOn('bothScored', svc)

#fig, ax = plt.subplots(figsize = (12, 8))
#ax.plot(range(len(res)), res)

#total = np.array(res)
#total = np.sum(total)
#print('total average = {0}%'.format(total / len(res)))










