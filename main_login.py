import requests
import json
from rich.progress import track
from rich import print
from threading import Thread
import qrcode
import time
import logging
from PIL import Image
from pyzbar.pyzbar import decode
from io import BytesIO
logging.basicConfig(level=logging.INFO)

# 😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆
print("[bold magenta]Made with ❤️ by tourkveg[/bold magenta]")
# 😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆😆

JSB_API_URL = "http://www.jingshibang.com/api/product/detail/"
PAPER_ID_BASE = 18935

# https://jsb2022-1253627302.cos.ap-beijing.myqcloud.com
JSB_STORAGE_HOST = input("storage host:")

# 微信登录二维码解析
WECHAT_AUTH = "http://www.jingshibang.com/api/wechat/pcauth2?wechat_flag="
QRCODE_API = "http://www.jingshibang.com/api/getwxpic"

USER_AGENT = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
# auth = input("auth:")
# cookies = input("cookies:")


def getQrCode() -> tuple[str, str]:
    res = requests.post(QRCODE_API, headers={
                        "User-Agent": USER_AGENT, "Referer": "http://www.jingshibang.com/home/?activeName=1"})
    res = json.loads(res.text)
    logging.debug(res)
    wechat_flag = res["data"]["weChatFlag"]
    pic_url = res["data"]["url"]
    logging.info(f"success!getQrCode")
    return wechat_flag, pic_url


def login() -> str:
    wechat_flag, pic_url = getQrCode()
    res = requests.get(pic_url, headers={"User-Agent": USER_AGENT})
    # with open("./qrcode.png","wb") as f:
    #     f.write(res.content)
    barcodes = decode(Image.open(BytesIO(res.content)))
    for barcode in barcodes:
        barcode_url = barcode.data.decode("utf-8")
    logging.debug(barcode_url)
    code = qrcode.QRCode()
    code.add_data(barcode_url)
    code.print_ascii(invert=False)
    while True:
        res = requests.get(WECHAT_AUTH+wechat_flag, headers={
                           "User-Agent": USER_AGENT, "Referer": "http://www.jingshibang.com/home/?activeName=1"})
        msg = json.loads(res.text)
        logging.debug(msg)
        if msg["status"] == 200:
            logging.info(f"[token]{msg['data']['token']}")
            logging.info("success!login")
            return msg["data"]["token"]
        time.sleep(1)


def getPaper(token: str, id: int) -> None:
    try:
        res = requests.get(url=JSB_API_URL+str(PAPER_ID_BASE+id), headers={
                           "User-Agent": USER_AGENT, "Referer": r"http://www.jingshibang.com/home/", "Authorization": "Bearer "+token, "Authori-Zation": "Bearer "+token}, timeout=3)
        res_data = json.loads(res.text)

        pdf_url = res_data["data"]["storeInfo"]["pdf_answer"]
        file_name = res_data["data"]["storeInfo"]["store_name"]
        pdf_file = JSB_STORAGE_HOST+pdf_url

        res_file = requests.get(pdf_file, timeout=3)
        with open(f"E:\\jingshibang\\{file_name}.pdf", "wb") as f:
            f.write(res_file.content)
            print(f"[{PAPER_ID_BASE+id}]")

    except Exception as e:
        print(f"[red]Exception#{PAPER_ID_BASE+id}[/red]")


PAPER_ID_START = 143030


token = login()

for i in track(range(PAPER_ID_START-PAPER_ID_BASE, 144975-PAPER_ID_BASE+1, 20), description="Downloading..."):
    threads = []

    for j in range(20):
        thread = Thread(target=getPaper, args=(token, i+j))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
