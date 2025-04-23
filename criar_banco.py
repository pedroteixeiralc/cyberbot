import sqlite3
from datetime import datetime

# Conecta (ou cria automaticamente) o banco bd.db
conn = sqlite3.connect('bd.db')
cursor = conn.cursor()

# Cria a tabela de promoções
cursor.execute('''
CREATE TABLE IF NOT EXISTS promocoes (
    id TEXT PRIMARY KEY,
    titulo TEXT,
    preco TEXT,
    link TEXT,
    data TEXT
)
''')

conn.commit()
conn.close()
print("✅ Banco de dados e tabela criados com sucesso!")
