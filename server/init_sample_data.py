"""
샘플 데이터 삽입 스크립트

데이터베이스 초기화(init_db.py) 후에 실행하여 
한국공학대학교 동아리 샘플 데이터를 생성합니다.

사용법:
    python init_sample_data.py
"""

import os
import pymysql
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def get_db_config():
    """환경 변수에서 데이터베이스 설정을 가져옵니다."""
    return {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD'),
        'database': os.environ.get('DB_NAME', 'club_db'),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

def insert_sample_data():
    """샘플 데이터를 데이터베이스에 삽입합니다."""
    config = get_db_config()
    
    print("=" * 60)
    print("📊 샘플 데이터 삽입을 시작합니다...")
    print("=" * 60)
    
    try:
        # MySQL 연결
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        print(f"\n📡 데이터베이스에 연결되었습니다. (DB: {config['database']})")
        
        # SQL 파일 경로
        sql_file_path = os.path.join(os.path.dirname(__file__), 'init_sample_data.sql')
        
        if not os.path.exists(sql_file_path):
            print(f"\n❌ SQL 파일을 찾을 수 없습니다: {sql_file_path}")
            return
        
        print(f"\n📄 SQL 파일을 읽는 중: {sql_file_path}\n")
        
        # SQL 파일 읽기 및 실행
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # 세미콜론으로 구분된 SQL 문 실행
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements, 1):
            # 주석 무시
            if statement.startswith('--') or not statement:
                continue
            
            try:
                cursor.execute(statement)
                # SELECT 문인 경우 결과 출력
                if statement.strip().upper().startswith('SELECT'):
                    results = cursor.fetchall()
                    if results:
                        for row in results:
                            for key, value in row.items():
                                print(f"   {key}: {value}")
                        print()
            except Exception as e:
                print(f"⚠️  경고 ({i}번째 구문): {str(e)[:100]}")
        
        # 변경사항 커밋
        connection.commit()
        
        print("\n" + "=" * 60)
        print("✅ 샘플 데이터 삽입이 완료되었습니다!")
        print("=" * 60)
        
        # 삽입된 데이터 통계
        print("\n📋 생성된 데이터 통계:")
        
        cursor.execute("SELECT COUNT(*) as count FROM Student")
        student_count = cursor.fetchone()['count']
        print(f"   - 학생: {student_count}명")
        
        cursor.execute("SELECT COUNT(*) as count FROM Club")
        club_count = cursor.fetchone()['count']
        print(f"   - 동아리: {club_count}개")
        
        cursor.execute("SELECT COUNT(*) as count FROM Post")
        post_count = cursor.fetchone()['count']
        print(f"   - 게시글: {post_count}개")
        
        cursor.execute("SELECT COUNT(*) as count FROM Belong")
        belong_count = cursor.fetchone()['count']
        print(f"   - 동아리 소속: {belong_count}건")
        
        cursor.execute("SELECT COUNT(*) as count FROM Apply")
        apply_count = cursor.fetchone()['count']
        print(f"   - 가입 신청: {apply_count}건")
        
        print("\n💡 테스트 계정 정보:")
        print("   - 관리자: admin / password123")
        print("   - 일반 학생: student01 / password123")
        print("   - 동아리 관리자: cod_admin / password123")
        
        print("\n🚀 이제 서버를 실행하고 로그인해보세요!")
        print("   python run.py\n")
        
    except pymysql.err.OperationalError as e:
        print(f"\n❌ 데이터베이스 연결 실패:")
        print(f"   {e}")
        print("\n💡 확인 사항:")
        print("   1. MySQL 서버가 실행 중인지 확인하세요.")
        print("   2. init_db.py를 먼저 실행했는지 확인하세요.")
        print("   3. .env 파일의 데이터베이스 설정을 확인하세요.")
        
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
    insert_sample_data()

