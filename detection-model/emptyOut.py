# For removing the pre-existing fields
import pandas as pd
import os

cwd = os.getcwd()
root=os.path.abspath(os.path.join(cwd, os.pardir))+"/dns-cache-poisoning"
print(root)

print("Reading Test Database")
df1=pd.read_csv(root+"/dataset/Webpages_Classification_test_data.csv")
# df1=df1.loc[:, ~df1.columns.str.match('Unnamed: ')]
# df1=df1.drop(["index", "url_len", "geo_loc", "tld", "who_is", "https", "js_len", "js_obf_len", "content"], axis=1)
df1=df1.drop("index", axis=1)
df1.to_csv(root+"/dataset/Webpages_Classification_test_data.csv")

print("Reading Training Database")
df2=pd.read_csv(root+"/dataset/Webpages_Classification_train_data.csv")
# df2=df2.loc[:, ~df2.columns.str.match('Unnamed: ')]
# df2=df2.drop(["index", "url_len", "geo_loc", "tld", "who_is", "https", "js_len", "js_obf_len", "content"], axis=1)
df2=df2.drop("index", axis=1)
df2.to_csv(root+"/dataset/Webpages_Classification_train_data.csv")
