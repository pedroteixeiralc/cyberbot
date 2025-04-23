import requests

# Substitua com o seu token real
TOKEN = '7568858647:AAEvggHZ1SsprSlPRSHIcFwH6lU657BFDHg'

# Pode ser o nome do canal (@nome) ou ID do grupo
CHAT_ID = -1002258489009


def enviar_para_telegram(mensagem):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': mensagem,
        'parse_mode': 'HTML'  # permite formatar com negrito, links, etc.
    }
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("✅ Enviado com sucesso!")
    else:
        print("❌ Erro ao enviar:", response.text)
