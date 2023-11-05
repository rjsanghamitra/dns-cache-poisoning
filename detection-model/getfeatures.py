import requests
import subprocess
import socket
import os
import pandas as pd

def is_HTTPS(url):
    try:
        response = requests.get(url)
        final_url = response.url
        return final_url, final_url.startswith("https")
    except Exception as e:
        print(e)
        return None, False

def get_features(url, ip):
    try:
        # Use the `nslookup` command to perform DNS lookup
        result = subprocess.check_output(["nslookup", url]).decode("utf-8")
        lines = result.split('\n')
        # Modify the line index to match the format of nslookup output
        line = lines[4] if len(lines) > 4 else ""
        parts = line.split()
        ttl = parts[2] if len(parts) > 2 else None
        # query_class = ""  # Not available from nslookup
        # record_type = ""  # Not available from nslookup
        url_len = len(url)
        # print(url)

        response = requests.get(url)
        a = url.split(".")
        tld = "." + a[-1]
        status_code = response.status_code
        final_url, is_https = is_HTTPS(url)
        try:
            ip_info = socket.getaddrinfo(ip, 0)
            ip_type = "Public" if not ip_info[0][4][0].startswith('127.') else "Private"
        except Exception as e:
            ip_type = "Private"

        # use the following
        # print(ttl) # time to live
        # print(query_class) # Not available from nslookup
        # print(record_type) # Not available from nslookup
        # print(url_len)
        # print(tld) # top-level domain
        # print(status_code)
        # print(final_url)
        # print(is_https)
        # print(ip_type) # public or private

        ans = [final_url, ip, url_len, tld, status_code, is_https, ip_type]
        return ans
    except Exception as e:
        return e
def main():
    # url = "http://www.google.com"  # Replace with your URL
    # ip = "127.0.0.1"  # Replace with your IP address

    cwd = os.getcwd()
    path=cwd+"/dataset/"
    df=pd.read_csv(path+"Webpages_Classification_test_data.csv")
    # urls=[]
    # ips=[]
    # url_len=[]
    # tld=[]
    # ttl=[]
    # qc=[]
    # rc=[]
    # sc=[]
    # https=[]
    # iptype=[]
    # labels=[]
    for url, ip, label in zip(df["url"], df["ip_add"], df["label"]):
        ans=get_features("http://"+url, ip)
        print(ans)
        try:
            urls.append(ans[0])
            ips.append(ans[1])
            url_len.append(ans[2])
            tld.append(ans[3])
            ttl.append(ans[4])
            qc.append(ans[5])
            rc.append(ans[6])
            sc.append(ans[7])
            https.append(ans[8])
            iptype.append(ans[9])
            labels.append(label)
        except Exception as e:
            continue
        
    # ans=[final_url, ip, url_len, tld, ttl, query_class, record_class, status_code, is_https, ip_type]
    df1=pd.DataFrame({
        "url": urls,
        "ip_add": ips,
        "url_len": url_len,
        "tld": tld,
        "ttl": ttl,
        "query_class": qc,
        "record_class": rc,
        "status_code": sc,
        "is_https": https,
        "ip_type": iptype,
        "label": labels,
    })
    df1.to_csv(path+"Test_Data.csv")

    # ans=get_features(url, ip)
    # print(ans)

if __name__ == "__main__":
    main()
