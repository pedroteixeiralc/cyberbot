import requests
from bs4 import BeautifulSoup

def listar_produtos_magalu():
    url = "https://www.magazinevoce.com.br/magazinecyberoffs/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erro ao acessar a página: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    produtos = soup.find_all("li", class_="sc-dkrFOg")

    if not produtos:
        print("Nenhum produto encontrado.")
        return

    for produto in produtos:
        nome = produto.find("h2")
        preco = produto.find("p", class_="sc-hlnMnd")  # Pode variar, confirmar no seu HTML
        imagem = produto.find("img")
        link_tag = produto.find("a", href=True)

        if nome and preco and link_tag:
            nome_produto = nome.text.strip()
            preco_produto = preco.text.strip()
            link = "https://www.magazinevoce.com.br" + link_tag['href']
            imagem_url = imagem['src'] if imagem else 'Imagem não encontrada'

            print("🛍️ Produto:", nome_produto)
            print("💰 Preço:", preco_produto)
            print("🖼️ Imagem:", imagem_url)
            print("🔗 Link:", link)
            print("-" * 60)

# Executar
listar_produtos_magalu()
