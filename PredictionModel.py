#Imports
import pandas as pd
import sklearn 
import numpy as np
import json

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

#Import Data
medData = pd.read_csv('C:/Users/Britn/OneDrive - Cal Poly Pomona/FRC Hackathon/healthcare_dataset.csv', encoding = 'ISO-8859-1')

#Removes empty rows/columns
medData.dropna(how='all')

#Data encoding
label_encoder = LabelEncoder()
medData['Gender'] = label_encoder.fit_transform(medData['Gender' ])
medData['Medical Condition'] = label_encoder.fit_transform(medData['Medical Condition' ])
medData['Insurance Provider'] = label_encoder.fit_transform(medData['Insurance Provider' ])
medData['Admission Type'] = label_encoder.fit_transform(medData['Admission Type' ])


#Preprocessing & Cleaning
x = medData.iloc[:,[1,2,3,5,6,7,11]]
y=medData.iloc[:, [12]]

x_clean = x.dropna()
y_clean = y.dropna()

x_clean = x_clean.loc[y_clean.index]

min_length = min(len(x), len(y))
x_clean = x[:min_length]
y_clean = y[:min_length]

#Data Split
x_train, x_test, y_train, y_test = train_test_split(x_clean, y_clean, test_size = 0.2, random_state = 42)
y_train = y_train.values.ravel()
y_test = y_test.values.ravel()


#Random Forest Implementation
rf = RandomForestClassifier(class_weight='balanced')
rf.fit(x_train, y_train)

y_pred = rf.predict(x_test)

#Results
accuracy = accuracy_score(y_test, y_pred)
print(f"Random Forest Classifier Accuracy: {accuracy*100:.4f}")
report = classification_report(y_test, y_pred)

#Export Json File
report_json = json.dumps(report, indent=4)
print(report_json)




