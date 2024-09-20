import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()
    env_mode = os.getenv('ENV_MODE')

    if env_mode == 'production':
        load_dotenv('.env.production')
    else:
        load_dotenv('.env.development')

load_environment()

DB_USER = os.getenv('DB_USER')
DB_PW = os.getenv('DB_PW')
DB_URL = os.getenv('DB_URL')
DB_NAME = os.getenv('DB_NAME')

SECRET_KEY=os.getenv('SECRET_KEY')
