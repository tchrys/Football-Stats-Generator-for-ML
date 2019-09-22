# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import keras

no_params = 54

def getMatrBigCsv(function, no_params):
    filename = 'csv_' + function
    names = []
    names.append('Result')
    for i in range(no_params):
        names.append(str(i + 1))
    data2 = pd.read_csv(filename, header = None, names = names)
    cols = data2.shape[1]
    X = data2.iloc[:,1:cols]
    y = data2.iloc[:,0:1]
    X = np.array(X.values)
    y = np.array(y.values)
    X_train, X_test, y_train, y_test = train_test_split(
                                    X, y, test_size=0.1, random_state=42)
    scaler = StandardScaler()
    X = scaler.fit_transform(X_train)
    Xt = scaler.fit_transform(X_test)
    return X, Xt, y_train, y_test
    
    
X, Xt, y, yt = getMatrBigCsv('homeWins', no_params)

Xv, X = X[:1000] , X[1000:]
yv, y = y[:1000], y[1000:]

#print(X)
#print(Xt.shape)


model = keras.models.Sequential([
        keras.layers.Dense(200, activation="relu"),
        keras.layers.Dense(30, activation="relu"),
        keras.layers.Dense(1, activation='sigmoid')
        ])
    
model.compile(loss = "binary_crossentropy", optimizer = "sgd",
              metrics = ["accuracy"])

history = model.fit(X, y, epochs = 15, validation_data = (Xv, yv))

pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1) # set the vertical range to [0-1]
plt.show()


X_new = Xt[:100]
y_proba = model.predict(X_new)
print(y_proba.round(2))










