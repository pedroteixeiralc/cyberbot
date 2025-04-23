# 🤖 Bot de Captura de Promoções de Afiliados (Em desenvolvimento)

Este script em Python coleta links e dados de promoções de diferentes plataformas de afiliados, com foco em integrar campanhas de Magalu, Shopee, Awin e Mercado Livre. A ideia é consolidar promoções e depois, opcionalmente, integrá-las com Telegram, sites ou outros canais.

## 📦 Plataformas Suportadas

- **Magalu (Magazine Você)**
- **Shopee**
- **Awin**
- **Mercado Livre**

## ⚙️ Pré-requisitos

- Python 3.7+
- Biblioteca `requests` instalada:
  ```bash
  pip install requests

🚀 Como usar
magalu_id = "cyberoffs"
shopee_app_id = "SUA_APP_ID"
shopee_secret = "SEU_SECRET"
awin_token = "SEU_TOKEN_OAUTH"
ml_id = "SEU_ID_AFILIADO"

🚀 Execute
python nome_do_arquivo.py

📂 Estrutura
pegar_promocoes_magalu()
Gera o link de afiliado Magalu (por enquanto apenas imprime o link).

pegar_promocoes_shopee()
Placeholder. Exige autenticação com assinatura HMAC — exemplo estrutural apenas.

pegar_promocoes_awin()
Exemplo de chamada real com token OAuth para consultar dados da API Awin.

pegar_promocoes_mercadolivre()
Apenas imprime o modelo de link de afiliado com ID.

⚠️ Observações
Shopee: exige autenticação via assinatura HMAC. A integração completa requer um fluxo de geração de token.

Magalu e Mercado Livre: atualmente exigem scraping ou uso de links de afiliado manualmente.

Awin: requer conta ativa e token OAuth para uso da API.

📲 Futuras Integrações
Envio das promoções por Telegram

Armazenamento em banco de dados ou planilhas

Painel web para visualização e curadoria

📜 Licença
Este projeto é de uso livre para estudos e testes. Para uso comercial, verifique as políticas de cada programa de afiliado.

Criado com 💻 por Pedro Lucas Carneiro Teixeira - Transformando Dados.
