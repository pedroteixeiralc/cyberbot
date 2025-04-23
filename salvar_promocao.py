import sqlite3
from datetime import datetime

# Conecta ao banco
conn = sqlite3.connect('bd.db')
cursor = conn.cursor()

# Promoção de teste
promo = {
    'id': 'teste123',
    'titulo': 'Mouse Gamer RGB',
    'preco': 'R$ 59,90',
    'link': 'https://promo.com.br/mouse',
    'data': datetime.now().isoformat()
}

# Verifica se já foi enviada
cursor.execute("SELECT 1 FROM promocoes WHERE id = ?", (promo['id'],))
if cursor.fetchone():
    print("⚠️ Promoção já existe.")
else:
    cursor.execute(
        "INSERT INTO promocoes (id, titulo, preco, link, data) VALUES (?, ?, ?, ?, ?)",
        (promo['id'], promo['titulo'], promo['preco'], promo['link'], promo['data'])
    )
    conn.commit()
    print("✅ Promoção salva com sucesso!")

conn.close()
