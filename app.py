import time
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

url = 'https://app.extended.exchange/api/v1/vault/public/summary'

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0'
}

cookies = {
    'x10_access_token': os.getenv("X10_ACCESS_TOKEN"),
    'x10_refresh_token': os.getenv("X10_REFRESH_TOKEN"),
    'AMP_MKTG_bb6bc63ee1': os.getenv("AMP_MKTG"),
    'AMP_bb6bc63ee1': os.getenv("AMP"),
    'AWSALBTG': os.getenv("AWSALBTG")
}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Erreur Telegram : {e}")

def monitoring_loop():
    alert_sent = False

    print("✅ Bot lancé. Attente d'alerte...")
    send_telegram_message("✅ Bot lancé, en attente d'alerte...")

    while True:
        try:
            response = requests.get(url, headers=headers, cookies=cookies)
            if response.status_code == 200:
                data = response.json().get("data", {})
                equity = float(data.get("equity", 0))
                equity_str = "${:,.2f}".format(equity)

                print(f"Vault: {equity_str}")

                if equity < 7_500_000 and not alert_sent:
                    message = f"🚨 Alerte : vault sous 7.5M ! Actuel : {equity_str}"
                    send_telegram_message(message)
                    os.system('say "Alerte vault sous sept millions cinq cent mille dollars"')
                    alert_sent = True
                elif equity >= 7_500_000 and alert_sent:
                    alert_sent = False  # Réarme l'alerte
            else:
                print(f"Erreur API : {response.status_code}")

        except Exception as e:
            print(f"❌ Exception : {e}")

        time.sleep(300)  # toutes les 5 minutes

if __name__ == "__main__":
    monitoring_loop()
