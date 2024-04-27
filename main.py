import requests
import json
from rich.progress import track

JSB_API_URL = "http://www.jingshibang.com/api/product/detail/"
PAPER_ID_BASE = 18935

# https://jsb2022-1253627302.cos.ap-beijing.myqcloud.com
JSB_STORAGE_HOST = input()

USER_AGENT = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
auth = r"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ3d3cuamluZ3NoaWJhbmcuY29tIiwiYXVkIjoid3d3LmppbmdzaGliYW5nLmNvbSIsImlhdCI6MTcxNDEzNTU0NywibmJmIjoxNzE0MTM1NTQ3LCJleHAiOjE3MTQ3NDAzNDcsImp0aSI6eyJpZCI6Nzc0NDY2LCJ0eXBlIjoid2VjaGF0In19.C3MA1-Mpn9GYsIs7FCb7oulZwNZHlJUXbItNqqKbi6Q"
cookies = r"auth.strategy=local3; auth._refresh_token.local3=false; PHPSESSID=e2684d7a6727b290857d6b5c0415e4df; cart_checked=%5B%5D; auth._token.local3=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ3d3cuamluZ3NoaWJhbmcuY29tIiwiYXVkIjoid3d3LmppbmdzaGliYW5nLmNvbSIsImlhdCI6MTcxNDEzNTU0NywibmJmIjoxNzE0MTM1NTQ3LCJleHAiOjE3MTQ3NDAzNDcsImp0aSI6eyJpZCI6Nzc0NDY2LCJ0eXBlIjoid2VjaGF0In19.C3MA1-Mpn9GYsIs7FCb7oulZwNZHlJUXbItNqqKbi6Q"

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
        print("[Exception]"+str(e))
        print("[data]"+str(PAPER_ID_BASE+i)+" "+str(res_data))