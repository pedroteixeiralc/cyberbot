import requests
import time

def buscar_ofertas_shopee():
    url = "https://shopee.com.br/api/v4/flash_sale/get_all_products?limit=100&need_personalize=true"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Referer": "https://shopee.com.br/flash_sale",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            itens = data.get("data", {}).get("items", [])

            if not itens:
                print("Nenhum produto encontrado.")
                return

            print("Produtos encontrados:")
            for item in itens:
                produto = item.get("item", {})
                nome = produto.get("name")
                preco = produto.get("price") / 100000  # conversão de centavos
                url_produto = f"https://shopee.com.br/{produto.get('name', '').replace(' ', '-')}-i.{produto.get('shopid')}.{produto.get('itemid')}"
                
                print(f"🛒 {nome}\n💰 R$ {preco:.2f}\n🔗 {url_produto}\n")

        else:
            print(f"Erro ao acessar a Shopee: {response.status_code}")
            print(response.text)

    except Exception as e:
        print("Erro ao acessar a Shopee:", e)

# Executa a função
buscar_ofertas_shopee()
