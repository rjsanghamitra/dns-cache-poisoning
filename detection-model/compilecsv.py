# For compiling the two datasets

import pandas as pd
import os

cwd=os.getcwd()
print("Reading Test Database")
df1=pd.read_csv(cwd+"/detection-model/Webpages_Classification_test_data.csv")
print("Reading Train Database")
df2=pd.read_csv(cwd+"/detection-model/Webpages_Classification_train_data.csv")

print("Compiling Databases")
pd.concat([df1, df2]).to_csv(cwd+'/detection-model/Webpages_Dataset_Final.csv', index=False)