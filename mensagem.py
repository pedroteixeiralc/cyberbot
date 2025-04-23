from telegram_bot import enviar_para_telegram

promo = {
    'titulo': 'Smart TV 50” 4K Samsung',
    'preco': 'R$ 2.199,00',
    'link': 'https://shopee.com.br/tv-samsung'
}

mensagem = f"""
<b>{promo['titulo']}</b>
💰 <b>Preço:</b> {promo['preco']}
🔗 <a href="{promo['link']}">Ver oferta</a>
"""

enviar_para_telegram(mensagem)
