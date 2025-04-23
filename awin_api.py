import requests
import sqlite3
from datetime import datetime
from config import Config
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('awin_api.log'),
        logging.StreamHandler()
    ]
)

class AwinAPI:
    @staticmethod
    def get_programs():
        """Obtém a lista de programas/afiliados disponíveis"""
        url = Config.BASE_URL + Config.programmes_endpoint()
        
        try:
            response = requests.get(
                url,
                headers=Config.HEADERS,
                params={'relationship': 'joined'}
            )
            response.raise_for_status()
            
            data = response.json()
            logging.debug(f"Resposta completa da API: {data}")
            
            # Verifica se a resposta é uma lista ou um dicionário
            if isinstance(data, list):
                logging.info(f"Programas obtidos com sucesso (formato lista). Total: {len(data)}")
                return {'data': data}
            elif isinstance(data, dict):
                logging.info(f"Programas obtidos com sucesso. Total: {len(data.get('data', []))}")
                return data
            else:
                logging.error(f"Formato de resposta inesperado: {type(data)}")
                return None
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao obter programas: {e}")
            if hasattr(e, 'response'):
                logging.error(f"Status code: {e.response.status_code}")
                logging.error(f"Resposta: {e.response.text}")
            return None

    @staticmethod
    def get_offers(program_id):
        """Obtém ofertas de um programa específico"""
        url = Config.BASE_URL + Config.offers_endpoint(program_id)
        
        try:
            response = requests.get(url, headers=Config.HEADERS)
            response.raise_for_status()
            
            data = response.json()
            logging.debug(f"Resposta completa de ofertas: {data}")
            
            # Verifica o formato da resposta
            if isinstance(data, list):
                logging.info(f"Ofertas obtidas (formato lista). Programa {program_id}. Total: {len(data)}")
                return {'data': data}
            elif isinstance(data, dict):
                logging.info(f"Ofertas obtidas. Programa {program_id}. Total: {len(data.get('data', []))}")
                return data
            else:
                logging.error(f"Formato de resposta inesperado: {type(data)}")
                return None
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao obter ofertas para programa {program_id}: {e}")
            return None

class DatabaseManager:
    @staticmethod
    def setup_database():
        """Configura o banco de dados SQLite"""
        conn = sqlite3.connect(Config.DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            offer_id TEXT UNIQUE,
            program_id TEXT,
            program_name TEXT,
            offer_name TEXT,
            description TEXT,
            terms TEXT,
            currency TEXT,
            default_track_uri TEXT,
            minimum_price REAL,
            maximum_price REAL,
            merchant_category TEXT,
            merchant_name TEXT,
            start_date TEXT,
            end_date TEXT,
            last_updated TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Índices para melhorar performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_offer_id ON offers(offer_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_program_id ON offers(program_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_merchant_name ON offers(merchant_name)')
        
        conn.commit()
        return conn

    @staticmethod
    def save_offers(conn, program_id, program_name, offers):
        """Salva ou atualiza ofertas no banco de dados"""
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        saved_count = 0
        updated_count = 0
        
        for offer in offers:
            # Verifica campos obrigatórios
            if not offer.get('id'):
                logging.warning("Oferta sem ID, pulando...")
                continue
                
            # Verifica se a oferta já existe
            cursor.execute('SELECT 1 FROM offers WHERE offer_id = ?', (offer.get('id'),))
            exists = cursor.fetchone()
            
            if exists:
                # Atualiza oferta existente
                cursor.execute('''
                UPDATE offers SET
                    program_id = ?,
                    program_name = ?,
                    offer_name = ?,
                    description = ?,
                    terms = ?,
                    currency = ?,
                    default_track_uri = ?,
                    minimum_price = ?,
                    maximum_price = ?,
                    merchant_category = ?,
                    merchant_name = ?,
                    start_date = ?,
                    end_date = ?,
                    last_updated = ?,
                    updated_at = ?
                WHERE offer_id = ?
                ''', (
                    program_id,
                    program_name,
                    offer.get('name', ''),
                    offer.get('description', ''),
                    offer.get('terms', ''),
                    offer.get('currency', ''),
                    offer.get('defaultTrackUri', ''),
                    offer.get('minimumPrice', 0),
                    offer.get('maximumPrice', 0),
                    offer.get('merchantCategory', ''),
                    offer.get('merchantName', ''),
                    offer.get('startDate', ''),
                    offer.get('endDate', ''),
                    offer.get('lastUpdated', ''),
                    now,
                    offer.get('id')
                ))
                updated_count += 1
            else:
                # Insere nova oferta
                cursor.execute('''
                INSERT INTO offers (
                    offer_id, program_id, program_name, offer_name, description, terms,
                    currency, default_track_uri, minimum_price, maximum_price,
                    merchant_category, merchant_name, start_date, end_date, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    offer.get('id'),
                    program_id,
                    program_name,
                    offer.get('name', ''),
                    offer.get('description', ''),
                    offer.get('terms', ''),
                    offer.get('currency', ''),
                    offer.get('defaultTrackUri', ''),
                    offer.get('minimumPrice', 0),
                    offer.get('maximumPrice', 0),
                    offer.get('merchantCategory', ''),
                    offer.get('merchantName', ''),
                    offer.get('startDate', ''),
                    offer.get('endDate', ''),
                    offer.get('lastUpdated', '')
                ))
                saved_count += 1
        
        conn.commit()
        logging.info(f"Ofertas salvas: {saved_count} novas, {updated_count} atualizadas")

def main():
    try:
        logging.info("Iniciando processo de sincronização com API Awin")
        
        # Configura banco de dados
        db_conn = DatabaseManager.setup_database()
        
        # Obtém programas
        programs_response = AwinAPI.get_programs()
        if not programs_response:
            logging.error("Nenhum programa encontrado ou erro ao acessar API")
            return
        
        # Obtém dados dos programas independente do formato
        programs_data = programs_response['data'] if 'data' in programs_response else programs_response
        
        if not programs_data:
            logging.warning("Nenhum programa disponível na resposta")
            return
        
        logging.info(f"Total de programas encontrados: {len(programs_data)}")
        
        # Para cada programa, obtém ofertas e salva no banco
        for program in programs_data:
            program_id = program.get('id')
            program_name = program.get('name', 'Sem nome')
            
            if not program_id:
                logging.warning("Programa sem ID, pulando...")
                continue
                
            logging.info(f"Processando programa: {program_name} (ID: {program_id})")
            
            offers_response = AwinAPI.get_offers(program_id)
            if not offers_response:
                logging.warning(f"Nenhuma oferta encontrada para o programa {program_name}")
                continue
                
            # Obtém dados das ofertas independente do formato
            offers_data = offers_response['data'] if 'data' in offers_response else offers_response
            if not offers_data:
                logging.warning(f"Nenhum dado de oferta para o programa {program_name}")
                continue
                
            DatabaseManager.save_offers(db_conn, program_id, program_name, offers_data)
        
        logging.info("Processo concluído com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}", exc_info=True)
    finally:
        if 'db_conn' in locals():
            db_conn.close()

if __name__ == '__main__':
    main()