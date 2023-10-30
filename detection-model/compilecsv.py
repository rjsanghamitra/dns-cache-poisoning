# For compiling the two datasets

import pandas as pd

df1=pd.read_csv("detection-model\\Webpages_Classification_test_data.csv")
df2=pd.read_csv("detection-model\\Webpages_Classification_train_data.csv")

pd.concat([df1, df2]).to_csv('detection-model\\Webpages_Dataset_Final.csv', index=False)