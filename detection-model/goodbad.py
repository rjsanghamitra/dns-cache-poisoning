# For setting good to 1, bad to 0 in the dataset in the labels column

import pandas as pd
import os

cwd=os.getcwd()
path=cwd+'/detection-model/'

dataset=path+'Webpages_Dataset_Final.csv'

print("Reading Database")
df=pd.read_csv(dataset)

print("Working on Database")
df['label']=df['label'].map(lambda x: 1 if x=='good' else 0)
df.to_csv(dataset, index=False)
