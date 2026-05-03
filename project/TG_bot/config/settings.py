import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "123123")
    DB_NAME = os.getenv("DB_NAME", "Barabulka")
    STATE_AIKATSU_PHOTO_ID = os.getenv("STATE_AIKATSU_PHOTO_ID")
    STATE_DWARVES_PHOTO_ID = os.getenv("STATE_DWARVES_PHOTO_ID")
    STATE_ICE_PHOTO_ID = os.getenv("STATE_ICE_PHOTO_ID")
    STATE_FIRE_PHOTO_ID = os.getenv("STATE_FIRE_PHOTO_ID")
    LOR_ID = os.getenv("LOR_ID")
    @staticmethod
    def db_dsn():
        return f"dbname={Config.DB_NAME} user={Config.DB_USER} password={Config.DB_PASSWORD} host={Config.DB_HOST} port={Config.DB_PORT}"
