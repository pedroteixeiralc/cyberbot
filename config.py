import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    API_KEY = os.getenv('AWIN_API_KEY')
    ADVERTISER_ID = os.getenv('AWIN_ADVERTISER_ID')
    BASE_URL = 'https://api.awin.com'
    
    # Database Configuration
    DB_NAME = 'awin_offers.db'
    
    # API Headers
    HEADERS = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    
    # API Endpoints
    @staticmethod
    def programmes_endpoint():
        return f'/publishers/{Config.ADVERTISER_ID}/programmes'
    
    @staticmethod
    def offers_endpoint(program_id):
        return f'/publishers/{Config.ADVERTISER_ID}/programmes/{program_id}/offers'