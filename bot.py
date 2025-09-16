import os
import requests
from bs4 import BeautifulSoup
import telegram
import time

# 🔑 Pegando variáveis de ambiente (configure no Replit em Secrets)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TOKEN)

# Função para coletar do Amostras Gratis
def coletar_amostrasgratis():
    try:
        url = "https://amostrasgratis.shop/"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            itens = [i.get_text(strip=True) for i in soup.find_all("h2")]
            if itens:
                return "🛍️ Amostras Grátis:\n\n" + "\n".join(itens[:5])
            else:
                return "Nenhuma amostra encontrada."
        else:
            return f"Erro {r.status_code} no site AmostrasGratis."
    except Exception as e:
        return f"Erro ao coletar AmostrasGratis: {e}"

# Função para coletar do Clube AG
def coletar_clubeag():
    try:
        url = "https://clubeag.com/"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            titulos = [t.get_text(strip=True) for t in soup.find_all("h2")]
            if titulos:
                return "📢 ClubeAG:\n\n" + "\n".join(titulos[:5])
            else:
                return "Nenhuma novidade no ClubeAG."
        else:
            return f"Erro {r.status_code} no site ClubeAG."
    except Exception as e:
        return f"Erro ao coletar ClubeAG: {e}"

# Loop infinito para checar novidades a cada X segundos
while True:
    try:
        msg1 = coletar_amostrasgratis()
        msg2 = coletar_clubeag()

        bot.send_message(chat_id=CHAT_ID, text=msg1)
        bot.send_message(chat_id=CHAT_ID, text=msg2)

        # Espera 1 hora antes de rodar de novo (3600 segundos)
        time.sleep(3600)
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"⚠️ Erro no bot: {e}")
        time.sleep(600)  # espera 10 minutos antes de tentar de novo
