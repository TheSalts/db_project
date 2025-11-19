"""
통합 데이터베이스 초기화 스크립트

데이터베이스 상태를 체크하고 필요에 따라 자동으로:
1. 데이터베이스 생성
2. 테이블 생성
3. 샘플 데이터 삽입

사용법:
    python init.py
    python init.py --skip-sample  # 샘플 데이터 없이
    python init.py --force        # 기존 데이터 삭제 후 재생성
"""

import os
import sys
import pymysql
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def get_db_config(include_db=True):
    """
    환경 변수에서 데이터베이스 설정을 가져옵니다.
    
    Args:
        include_db: 데이터베이스명 포함 여부
    """
    config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD'),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    if include_db:
        config['database'] = os.environ.get('DB_NAME', 'club_db')
    
    return config

def check_database_exists(cursor, db_name):
    """데이터베이스가 존재하는지 확인합니다."""
    cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
    return cursor.fetchone() is not None

def check_tables_exist(cursor):
    """테이블이 존재하는지 확인합니다."""
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return len(tables) > 0

def check_data_exists(cursor):
    """데이터가 존재하는지 확인합니다."""
    cursor.execute("SELECT COUNT(*) as count FROM Student")
    student_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM Club")
    club_count = cursor.fetchone()['count']
    
    return student_count > 0 or club_count > 0

def execute_sql_file(cursor, filepath, description):
    """SQL 파일을 읽고 실행합니다."""
    print(f"\n📄 {description}...")
    
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
    success_count = 0
    for statement in statements:
        statement = statement.strip()
        if statement and not statement.startswith('SELECT'):
            try:
                cursor.execute(statement)
                success_count += 1
            except Exception as e:
                # INSERT IGNORE 등으로 중복 에러는 무시
                if 'Duplicate entry' not in str(e):
                    print(f"   ⚠️  경고: {str(e)[:80]}")
    
    print(f"   ✓ {success_count}개 구문 실행 완료")
    return success_count > 0

def print_statistics(cursor):
    """현재 데이터 통계를 출력합니다."""
    print("\n📊 현재 데이터베이스 상태:")
    
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

def init_database():
    """데이터베이스를 초기화합니다."""
    # 명령줄 인자 처리
    skip_sample = '--skip-sample' in sys.argv
    force = '--force' in sys.argv
    
    config = get_db_config(include_db=False)
    db_name = os.environ.get('DB_NAME', 'club_db')
    
    print("=" * 70)
    print("🗄️  동아리 플랫폼 데이터베이스 초기화")
    print("=" * 70)
    
    try:
        # MySQL 연결 (데이터베이스 선택 없이)
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        print(f"\n📡 MySQL 서버에 연결되었습니다. (호스트: {config['host']})")
        
        # 1. 데이터베이스 존재 확인
        db_exists = check_database_exists(cursor, db_name)
        
        if db_exists:
            print(f"\n✓ 데이터베이스 '{db_name}'가 이미 존재합니다.")
            cursor.execute(f"USE {db_name}")
            
            # 테이블 존재 확인
            tables_exist = check_tables_exist(cursor)
            
            if tables_exist:
                print("✓ 테이블이 이미 존재합니다.")
                
                # 데이터 존재 확인
                data_exists = check_data_exists(cursor)
                
                if data_exists:
                    if force:
                        print("\n⚠️  --force 옵션: 기존 데이터를 삭제하고 재생성합니다.")
                        # 테이블 재생성을 위해 스키마 재실행
                        sql_file = os.path.join(os.path.dirname(__file__), 'init_db.sql')
                        execute_sql_file(cursor, sql_file, "테이블 재생성 중")
                        connection.commit()
                    else:
                        print("✓ 데이터가 이미 존재합니다.")
                        print("\n💡 기존 데이터베이스를 사용합니다.")
                        print_statistics(cursor)
                        print("\n⚠️  초기화하려면 --force 옵션을 사용하세요:")
                        print("   python init.py --force")
                        return
                else:
                    print("ℹ️  데이터가 없습니다. 샘플 데이터를 생성합니다.")
            else:
                print("ℹ️  테이블이 없습니다. 테이블을 생성합니다.")
                # 스키마 생성
                sql_file = os.path.join(os.path.dirname(__file__), 'init_db.sql')
                execute_sql_file(cursor, sql_file, "테이블 생성 중")
                connection.commit()
        else:
            print(f"\nℹ️  데이터베이스 '{db_name}'가 없습니다. 새로 생성합니다.")
            # 스키마 생성
            sql_file = os.path.join(os.path.dirname(__file__), 'init_db.sql')
            execute_sql_file(cursor, sql_file, "데이터베이스 및 테이블 생성 중")
            connection.commit()
            cursor.execute(f"USE {db_name}")
        
        # 2. 샘플 데이터 삽입 (skip_sample이 아닌 경우)
        if not skip_sample:
            print("\n" + "=" * 70)
            print("📊 샘플 데이터 생성")
            print("=" * 70)
            
            sample_file = os.path.join(os.path.dirname(__file__), 'init_sample_data.sql')
            
            if os.path.exists(sample_file):
                execute_sql_file(cursor, sample_file, "샘플 데이터 삽입 중")
                connection.commit()
            else:
                print("⚠️  샘플 데이터 파일을 찾을 수 없습니다.")
        else:
            print("\n⏭️  샘플 데이터 삽입을 건너뜁니다. (--skip-sample)")
        
        # 3. 최종 통계 출력
        print("\n" + "=" * 70)
        print("✅ 데이터베이스 초기화가 완료되었습니다!")
        print("=" * 70)
        
        print_statistics(cursor)
        
        if not skip_sample:
            print("\n💡 테스트 계정:")
            print("   - 사이트 관리자: admin / password123")
            print("   - 일반 학생: student01 / password123")
            print("   - 동아리 관리자: cod_admin / password123")
        
        print("\n🚀 이제 서버를 실행할 수 있습니다:")
        print("   python run.py\n")
        
    except pymysql.err.OperationalError as e:
        print(f"\n❌ 데이터베이스 연결 실패:")
        print(f"   {e}")
        print("\n💡 확인 사항:")
        print("   1. MySQL 서버가 실행 중인지 확인하세요.")
        print("   2. .env 파일의 데이터베이스 설정을 확인하세요.")
        print("      - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME")
        print("   3. 데이터베이스 사용자의 권한을 확인하세요.")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        if connection:
            connection.rollback()
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("\n🔌 데이터베이스 연결이 종료되었습니다.\n")

if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
동아리 플랫폼 데이터베이스 초기화 스크립트

사용법:
    python init.py              # 기본: DB 체크 후 자동 초기화
    python init.py --skip-sample  # 샘플 데이터 없이 초기화
    python init.py --force        # 기존 데이터 삭제 후 재생성
    python init.py --help         # 도움말 표시

설명:
    이 스크립트는 데이터베이스 상태를 자동으로 체크하고:
    - DB가 없으면 생성
    - 테이블이 없으면 생성
    - 데이터가 없으면 샘플 데이터 삽입
    - 데이터가 있으면 건너뛰기 (--force로 재생성 가능)
""")
    else:
        init_database()

