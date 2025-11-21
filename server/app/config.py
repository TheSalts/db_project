# app/config.py
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """Flask 앱 설정을 위한 Config 클래스"""
    
    # DB 접속 정보
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME', 'club_db')
    
    # JWT 설정
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = int(os.environ.get('JWT_EXPIRATION_HOURS', '24'))  # 기본 24시간