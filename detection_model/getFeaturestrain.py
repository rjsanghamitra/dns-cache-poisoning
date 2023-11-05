import requests
import socket
import os
import pandas as pd
import subprocess

def is_HTTPS(url):
    try:
        response=requests.get(url)
        final_url=response.url
        return final_url, final_url.startswith("https")
    except Exception as e:
        return None, False

def getFeatures(url, ip):
    try:
        result=subprocess.check_output(["nslookup", url]).decode("utf-8")
        lines=result.split('\n')
        line=lines[4] if len(lines)>4 else ""
        parts=line.split()
        url_len=len(url)
        response=requests.get(url)
        a=url.split(".")
        tld="."+a[-1]
        status_code=response.status_code
        final_url, ishttps= is_HTTPS(url)
        try:
            ip_info=socket.getaddrinfo(ip, 0)
            ip_type="Public" if not ip_info[0][4][0].startswith('127.') else "Private"
        except Exception as e:
            ip_type="Private"
        ans=[final_url, ip, url_len, tld, status_code, ishttps, ip_type]
        return ans
    except Exception as e:
        return e
 
def main():
    cwd=os.getcwd()
    df=pd.read_csv(cwd+"/dataset/Webpages_Classification_train_data.csv")
    # df1=pd.DataFrame(columns=["url", "ip_add", "url_len", "tld", "status_code", "is_https", "ip_type", "label"])
    df.drop()
    entries.to_csv(cwd+"/Train_Dataset.csv", index=False)

if __name__ == "__main__":
    main()