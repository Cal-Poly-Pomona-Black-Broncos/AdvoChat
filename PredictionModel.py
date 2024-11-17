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

#Data Cleaning & Preprocessing
medData = pd.read_csv('C:/Users/Britn/OneDrive - Cal Poly Pomona/FRC Hackathon/healthcare_dataset.csv', encoding = 'ISO-8859-1')
medData.dropna(how='all')

label_encoder = LabelEncoder()
medData['Gender'] = label_encoder.fit_transform(medData['Gender' ])
medData['Medical Condition'] = label_encoder.fit_transform(medData['Medical Condition' ])
medData['Insurance Provider'] = label_encoder.fit_transform(medData['Insurance Provider' ])
medData['Admission Type'] = label_encoder.fit_transform(medData['Admission Type' ])


#Data Split
x = medData.iloc[:,[1,2,3,5,6,7,11]]
y=medData.iloc[:, [12]]

x_clean = x.dropna()
y_clean = y.dropna()

x_clean = x_clean.loc[y_clean.index]

min_length = min(len(x), len(y))
x_clean = x[:min_length]
y_clean = y[:min_length]


x_train, x_test, y_train, y_test = train_test_split(x_clean, y_clean, test_size = 0.2, random_state = 42)
y_train = y_train.values.ravel()
y_test = y_test.values.ravel()


#Random Forest Model
rf = RandomForestClassifier(class_weight='balanced')
rf.fit(x_train, y_train)

y_pred = rf.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Random Forest Classifier Accuracy: {accuracy*100:.4f}")
report = classification_report(y_test, y_pred)

report_json = json.dumps(report, indent=4)

# dictionary to store encoders for categorical columns
encoders = {}

# =categorical columns
categorical_columns = ['Gender', 'Medical Condition', 'Insurance Provider', 'Admission Type']

# LabelEncoders for each categorical column
for col in categorical_columns:
    encoder = LabelEncoder()
    medData[col] = encoder.fit_transform(medData[col])
    encoders[col] = encoder

def handle_unseen_category(encoder, value):
    if value in encoder.classes_:
        return encoder.transform([value])[0]  # Transform and return the encoded value
    else:
        return -1


def predict_hospital(model, x_clean, user_input, encoders):
    input_df = pd.DataFrame([user_input], columns=x_clean.columns)

    
    for col in input_df.columns:
        if col in encoders:  
            encoder = encoders[col]
            value = input_df[col].iloc[0]  
            encoded_value = handle_unseen_category(encoder, value)
            input_df[col] = encoded_value
    prediction = model.predict(input_df)
    return prediction

#Test
user_input = [20, 'Male', 'Cancer', 'Medicare', 18856.28131, 'Urgent', 10 ]

print(predict_hospital(rf, x_clean, user_input, encoders))

