import pandas as pd
import sklearn as sk
import numpy as np

medData = pd.read_csv('C:/Users/Britn/OneDrive - Cal Poly Pomona/FRC Hackathon/healthcare_dataset.csv')

x = medData.iloc[:,[1,2,3,5,6,7,11,12]]
x_clean = x.dropna(how='all')

print(x_clean)



