# app/utils/db.py
import pymysql
from flask import current_app

def get_db_connection():
    """DB 커넥션을 반환하는 함수"""
    try:
        connection = pymysql.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME'],
            charset='utf8mb4',
            # 결과를 Python 딕셔너리 형태로 받기 위한 설정
            cursorclass=pymysql.cursors.DictCursor  
        )
        return connection
    except Exception as e:
        print(f"DB 연결 오류 발생: {e}")
        return None