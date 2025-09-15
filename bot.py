import requests
from bs4 import BeautifulSoup
import time

import os

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

URL_SITE = "https://amostrasgratis.shop/"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def check_updates(last_title):
    r = requests.get(URL_SITE)
    soup = BeautifulSoup(r.text, "html.parser")

    latest_post = soup.find("h2", class_="entry-title")  # busca o título do último post
    if latest_post:
        title = latest_post.get_text().strip()
        link = latest_post.find("a")["href"]

        if title != last_title:  # só envia se for novidade
            send_message(f"🚨 Nova amostra grátis!\n{title}\n{link}")
            return title
    return last_title

def main():
    last_title = ""
    while True:
        try:
            last_title = check_updates(last_title)
        except Exception as e:
            print("Erro:", e)
        time.sleep(60)  # espera 1 minuto antes de verificar de novo

if __name__ == "__main__":
    main()

