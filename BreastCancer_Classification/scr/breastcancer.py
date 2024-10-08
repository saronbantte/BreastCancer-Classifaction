# -*- coding: utf-8 -*-
"""BreastCancer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uAt3oBG_3vOxC2oMu3nkum4UFVxNszkX
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BreastCancer=pd.read_csv('/content/drive/MyDrive/BreastCancer.csv')

BreastCancer.head()

BreastCancer.info()

BreastCancer.isna().sum()

BreastCancer.describe()

Corr=BreastCancer.corr()
Corr

Corr['target'].sort_values(ascending=False)

BreastCancer.columns

features, target= BreastCancer.drop('target', axis=1), BreastCancer['target']

features.info()

columns=BreastCancer.columns
sns.heatmap(BreastCancer[columns[:10]].corr(), annot= True, cmap='Blues')

# LETS GET TO PLOTTING OF THE DATA
sns.scatterplot(x='mean radius', y='mean compactness', hue='target',data=BreastCancer)

"""Okay this is going to give you the main goal of this project:In this data we are given the features of a tumor in the breast and we need to identify if this tumor is cancerous or not. based on the given data we will predict if the tumor is beningn or malignant for a new and unseen data. using this historic data first we do some EDA and form ther we build a model that will bw able to identify the state of teh tumor. In EAD we will use some cool visulaization to idntify some patterns that can help to grap some insights from the historical data."""

sns.scatterplot(x='mean area', y='mean concave points', hue='target', data=BreastCancer)

sns.scatterplot(x='mean radius', y='mean perimeter', hue='target', data=BreastCancer)

columns=BreastCancer.columns
column=BreastCancer[columns[:10]]
for col in column:
  sns.boxplot(x=BreastCancer['target'], y= BreastCancer[col], hue='target', data=BreastCancer)
  plt.xlabel('Target')
  plt.ylabel(col)
  plt.title(f'Boxplot of Target vs {col} ')
  plt.show()

"""In general we can say that a small, simpler and less dense tumor is more likely going to be a cancerous tumor. Lokking at some details of the feature.

1, The radius and density of the tumour a benign tumor is much compact and has a bigger radius.
2,The mean concavity points of the tumor and the mean area benign tumor has high mean concavity points and bigger area compared to a maligant tumor.

the other thing to consider is using boxplots to identify if there is a major difference between the targets based on the features. based on the mean radius, area, perimeter, compactness, and concavity there is a clear difference betweeen the tumors. based on mean smoothness and fractal dimension are not telling anything if there is a difference.
"""



"""Now i want to compare how the mean values of tumors considered malignat with the worst case value sof a tumor."""

BreastCancer.columns

BreastCancer.head()

Columns=BreastCancer.columns
sns.heatmap(BreastCancer[Columns[20:30]].corr(), annot=True, cmap='Blues')
plt.show()

"""Comparing the malignanat and benign tumors on the worst possible feature value."""

columns=BreastCancer[Columns[20:30]]
for col in columns:
  sns.boxplot(x='target',y=BreastCancer[col], hue='target', data=BreastCancer )
  plt.xlabel('Target')
  plt.ylabel(col)
  plt.title(f' Boxplot of Target vs {col}')
  plt.show()

import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score, log_loss
from sklearn.model_selection import cross_val_score, cross_validate, cross_val_predict

x_train, x_test, y_train, y_test=train_test_split(features, target, test_size=0.2, random_state=42)

from sklearn.model_selection import GridSearchCV
pipeline=Pipeline([('scaler', StandardScaler()),('LR', LogisticRegression())])
param_grid = {
    'LR__penalty': ['l1', 'l2'],
    'LR__solver': ['lbfgs', 'sag', 'saga'],
    'LR__max_iter': [50, 100, 150],
    'LR__C': [1.0, 1.5, 0.5]
}
model=GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', verbose=1)
model.fit(x_train, y_train)
print(model.best_params_)
best_model=model.best_estimator_
yhat=best_model.predict(x_test)
print(classification_report(y_test, yhat))
ConfusionMatrixDisplay.from_predictions(y_test, yhat)
plt.show()

Accuracy=cross_val_score(best_model, x_train, y_train, cv=5, scoring='accuracy')
Precision=cross_val_score(best_model, x_train, y_train, cv=5, scoring='precision')
Recall=cross_val_score(best_model, x_train, y_train, cv=5, scoring='recall')
F1_score=cross_val_score(best_model, x_train, y_train, cv=5, scoring='f1')
yhat_prob=cross_val_predict(best_model, x_train, y_train, cv=5, method='predict_proba')
roc_curv=sklearn.metrics.roc_curve(y_train, yhat_prob[:,1])# this is recall against FPT so the prdication prob should be only the positive area.
plt.plot(roc_curv[0], roc_curv[1])
plt.show()
metrics={'Accuracy':Accuracy.mean(), 'Precision':Precision.mean(), 'Recall':Recall.mean(), 'F1_score':F1_score.mean()}
Metrics=pd.DataFrame(metrics, index=[0])
Metrics.stack()
Metrics.columns=['metric','value']

"""Okay looks like the logistic Regression model performed very well on the classification task. look at the performace measures. Now the problem is we have features indicating the error of each measuresment. How can that be use to find some good insights. TIME to think about how we can we use it.

"""

yhat_prob=best_model.predict_proba(x_test)
log_Loss=log_loss(y_test,yhat_prob)
log_Loss

"""The value of the log loss is indicating the good model performance."""

from sklearn.model_selection import learning_curve
train_size, train_score, validation_score=learning_curve(best_model, x_train, y_train, cv=5, scoring='neg_log_loss',train_sizes=np.linspace(0.1, 1,10))# starting form 10% of the data to 100%
train_score_mean=-train_score.mean(axis=1)
validation_score_mean=-validation_score.mean(axis=1)
plt.plot(train_size, train_score_mean, label='Training Score')
plt.plot(train_size, validation_score_mean, label='Validation Score')
plt.legend()
plt.show()

"""Looking at the learning curves, when the traning size is small the traning score is also small a but the validation score is high indicating overfitting, as the traning size incease the gap between the traning and validation score decreases which shows a good generalization."""



BreastCancer.shape

import joblib
joblib.dump(best_model, 'model.pkl')

breast_cancer_classifer = joblib.load('model.pkl')

new_breast_cancer_data=pd.read_csv('/content/drive/MyDrive/BreastCancer.csv')
new_breast_cancer_data.drop('target', axis=1, inplace=True)

new_breast_cancer_data.head()

prediction=breast_cancer_classifer.predict(new_breast_cancer_data)
prediction

