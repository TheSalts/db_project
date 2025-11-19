"""
데이터베이스 초기화 스크립트

이 스크립트는 MySQL 데이터베이스를 초기화하고 테이블을 생성합니다.
실행 전 .env 파일에 데이터베이스 설정이 올바르게 되어 있는지 확인하세요.

사용법:
    python init_db.py
"""

import os
import pymysql
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def get_db_config():
    """
    환경 변수에서 데이터베이스 설정을 가져옵니다.
    """
    return {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD'),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

def execute_sql_file(cursor, filepath):
    """
    SQL 파일을 읽고 실행합니다.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        sql_content = file.read()
    
    # DELIMITER로 구분된 부분 처리
    statements = []
    current_statement = []
    in_delimiter_block = False
    
    for line in sql_content.split('\n'):
        line = line.strip()
        
        # DELIMITER 명령 처리
        if line.startswith('DELIMITER'):
            if '$$' in line:
                in_delimiter_block = True
            else:
                in_delimiter_block = False
            continue
        
        # 주석 무시
        if line.startswith('--') or not line:
            continue
        
        current_statement.append(line)
        
        # 구문 종료 감지
        if in_delimiter_block:
            if line.endswith('$$'):
                statements.append('\n'.join(current_statement)[:-2])  # $$ 제거
                current_statement = []
                in_delimiter_block = False
        else:
            if line.endswith(';'):
                statements.append('\n'.join(current_statement))
                current_statement = []
    
    # 남은 구문 추가
    if current_statement:
        statements.append('\n'.join(current_statement))
    
    # 각 구문 실행
    for statement in statements:
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
                print(f"✓ 실행 완료: {statement[:50]}...")
            except Exception as e:
                print(f"✗ 오류 발생: {statement[:50]}...")
                print(f"  에러 메시지: {e}")

def init_database():
    """
    데이터베이스를 초기화합니다.
    """
    config = get_db_config()
    
    print("=" * 60)
    print("🗄️  데이터베이스 초기화를 시작합니다...")
    print("=" * 60)
    
    try:
        # MySQL 연결 (데이터베이스 선택 없이)
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        print(f"\n📡 MySQL 서버에 연결되었습니다. (호스트: {config['host']})")
        
        # SQL 파일 경로
        sql_file_path = os.path.join(os.path.dirname(__file__), 'init_db.sql')
        
        if not os.path.exists(sql_file_path):
            print(f"\n❌ SQL 파일을 찾을 수 없습니다: {sql_file_path}")
            return
        
        print(f"\n📄 SQL 파일을 읽는 중: {sql_file_path}")
        print("\n" + "=" * 60)
        print("SQL 구문 실행 중...")
        print("=" * 60 + "\n")
        
        # SQL 파일 실행
        execute_sql_file(cursor, sql_file_path)
        
        # 변경사항 커밋
        connection.commit()
        
        print("\n" + "=" * 60)
        print("✅ 데이터베이스 초기화가 완료되었습니다!")
        print("=" * 60)
        
        # 생성된 테이블 확인
        cursor.execute("USE club_db")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("\n📋 생성된 테이블 목록:")
        for table in tables:
            table_name = list(table.values())[0]
            print(f"   - {table_name}")
        
        print("\n💡 이제 'python run.py' 명령으로 서버를 실행할 수 있습니다.\n")
        
    except pymysql.err.OperationalError as e:
        print(f"\n❌ 데이터베이스 연결 실패:")
        print(f"   {e}")
        print("\n💡 확인 사항:")
        print("   1. MySQL 서버가 실행 중인지 확인하세요.")
        print("   2. .env 파일의 데이터베이스 설정을 확인하세요.")
        print("   3. 데이터베이스 사용자의 권한을 확인하세요.")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        connection.rollback()
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("\n🔌 데이터베이스 연결이 종료되었습니다.\n")

if __name__ == '__main__':
    init_database()

