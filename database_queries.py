import sqlite3
import csv
from datetime import datetime
from config import Config
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class QueryManager:
    @staticmethod
    def get_connection():
        """Estabelece conexão com o banco de dados"""
        try:
            conn = sqlite3.connect(Config.DB_NAME)
            conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
            return conn
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            return None

    @staticmethod
    def get_offers_by_program(program_id, limit=100):
        """Obtém ofertas por programa"""
        conn = QueryManager.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT offer_id, offer_name, merchant_name, minimum_price, currency 
            FROM offers 
            WHERE program_id = ?
            LIMIT ?
            ''', (program_id, limit))
            
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar ofertas: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def export_to_csv(query, params=None, filename=None):
        """Exporta resultados de consulta para CSV"""
        if not filename:
            filename = f"offers_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
        conn = QueryManager.get_connection()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Escreve cabeçalho
                writer.writerow([description[0] for description in cursor.description])
                # Escreve dados
                writer.writerows(cursor.fetchall())
                
            logging.info(f"Dados exportados com sucesso para {filename}")
            return True
        except Exception as e:
            logging.error(f"Erro ao exportar: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_recent_offers(days=7, limit=50):
        """Obtém ofertas recentemente atualizadas"""
        conn = QueryManager.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT offer_id, offer_name, merchant_name, last_updated 
            FROM offers 
            WHERE date(last_updated) >= date('now', ?)
            ORDER BY last_updated DESC
            LIMIT ?
            ''', (f'-{days} days', limit))
            
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar ofertas recentes: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_merchant_stats():
        """Obtém estatísticas por merchant"""
        conn = QueryManager.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT 
                merchant_name,
                COUNT(*) as offer_count,
                AVG(minimum_price) as avg_min_price,
                AVG(maximum_price) as avg_max_price
            FROM offers
            GROUP BY merchant_name
            ORDER BY offer_count DESC
            ''')
            
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar estatísticas: {e}")
            return None
        finally:
            conn.close()

if __name__ == '__main__':
    # Exemplo de uso
    print("=== Últimas ofertas atualizadas ===")
    recent_offers = QueryManager.get_recent_offers()
    for offer in recent_offers or []:
        print(f"{offer['offer_name']} - {offer['merchant_name']} ({offer['last_updated']})")
    
    print("\n=== Estatísticas por merchant ===")
    stats = QueryManager.get_merchant_stats()
    for stat in stats or []:
        print(f"{stat['merchant_name']}: {stat['offer_count']} ofertas")
    
    # Exportar todas as ofertas para CSV
    QueryManager.export_to_csv("SELECT * FROM offers")