import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '123123')
    DB_NAME = os.getenv('DB_NAME', 'Barabulka')

    @staticmethod
    def db_dsn():
        return f"dbname={Config.DB_NAME} user={Config.DB_USER} password={Config.DB_PASSWORD} host={Config.DB_HOST} port={Config.DB_PORT}"
