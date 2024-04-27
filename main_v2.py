import requests
import json
from rich.progress import track
from threading import Thread

JSB_API_URL = "http://www.jingshibang.com/api/product/detail/"
PAPER_ID_BASE = 18935

# https://jsb2022-1253627302.cos.ap-beijing.myqcloud.com
JSB_STORAGE_HOST = input("storage host:")

USER_AGENT = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
auth = input("auth:")
cookies = input("cookies:")

'''
for i in track(range(21235-PAPER_ID_BASE,(149975-PAPER_ID_BASE)),description="Downloading..."):
    try:
        res = requests.get(url = JSB_API_URL+str(PAPER_ID_BASE+i), headers={"User-Agent":USER_AGENT,"Cookie":cookies,"Referer":r"http://www.jingshibang.com/home/","Authorization":auth,"Authori-Zation":auth},timeout=3)
        res_data = json.loads(res.text)

        pdf_url = res_data["data"]["storeInfo"]["pdf_answer"]
        file_name = res_data["data"]["storeInfo"]["store_name"]
        pdf_file = JSB_STORAGE_HOST+pdf_url

        res_file = requests.get(pdf_file,timeout=3)
        with open(f"./files/{file_name}.pdf","wb") as f:
            f.write(res_file.content)
            print(PAPER_ID_BASE+i)
    except Exception as e:
        print("[Exception]"+strc(e))
        print("[data]"+str(PAPER_ID_BASE+i)+" "+str(res_data))
'''

def getPaper(id):
    try:
        res = requests.get(url = JSB_API_URL+str(PAPER_ID_BASE+id), headers={"User-Agent":USER_AGENT,"Cookie":cookies,"Referer":r"http://www.jingshibang.com/home/","Authorization":auth,"Authori-Zation":auth},timeout=3)
        res_data = json.loads(res.text)

        pdf_url = res_data["data"]["storeInfo"]["pdf_answer"]
        file_name = res_data["data"]["storeInfo"]["store_name"]
        pdf_file = JSB_STORAGE_HOST+pdf_url

        res_file = requests.get(pdf_file,timeout=3)
        with open(f"./files/{file_name}.pdf","wb") as f:
            f.write(res_file.content)
            print(f"[{PAPER_ID_BASE+id}]")
    except Exception as e:
        print(f"[Exception# {PAPER_ID_BASE+id}]")

# i = 119000-PAPER_ID_BASE


for i in track(range(PAPER_ID_BASE,144975-PAPER_ID_BASE+1,20),description="Downloading..."):
#while i<=144975-PAPER_ID_BASE:
    threads = []
    for j in range(20):
        #print(i+j)
        thread = Thread(target=getPaper,args=(i+j,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
