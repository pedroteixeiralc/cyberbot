import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('awin_offers.db')
cursor = conn.cursor()

# Executar consulta
cursor.execute("SELECT * FROM offers LIMIT 5")

# Obter resultados
results = cursor.fetchall()
for row in results:
    print(row)

# Fechar conexão
conn.close()