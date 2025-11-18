# app/services/auth_service.py
import pymysql
import bcrypt
from app.utils.db import get_db_connection

def create_user(data):
    """새로운 학생(유저)을 생성합니다."""
    
    # 비밀번호 해시
    password = data['Pw'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    conn = None
    cursor = None
    
    sql = """
        INSERT INTO Student (Student_ID, Login_ID, Pw, Name, phone_num, Email)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(sql, (
            data['Student_ID'],
            data['Login_ID'],
            hashed_password, # 해시된 비밀번호 저장
            data['Name'],
            data.get('phone_num'), # 선택적 필드
            data.get('Email')      # 선택적 필드
        ))
        
        conn.commit()
        return True, "회원가입 성공"
        
    except pymysql.err.IntegrityError as e:
        # UNIQUE 제약조건 위반 (학번, 로그인ID, 이메일 중복)
        error_code, error_message = e.args
        if error_code == 1062: # Duplicate entry
            if 'UK_Login_ID' in error_message:
                return False, "이미 사용 중인 아이디입니다."
            if 'UK_Email' in error_message:
                return False, "이미 사용 중인 이메일입니다."
            if 'PRIMARY' in error_message:
                return False, "이미 등록된 학번입니다."
        return False, "데이터베이스 오류"
        
    except Exception as e:
        print(f"유저 생성 오류: {e}")
        return False, "서버 오류 발생"
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_user_by_login_id(login_id):
    """Login_ID로 유저 정보를 가져옵니다 (로그인 시 사용)."""
    
    conn = None
    cursor = None
    
    # 비밀번호(Pw)와 학번(Student_ID)만 가져옴
    sql = "SELECT Student_ID, Pw FROM Student WHERE Login_ID = %s"
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor() # DictCursor가 적용됨 (db.py에서 설정)
        
        cursor.execute(sql, (login_id,))
        user = cursor.fetchone() # 딕셔너리 형태로 유저 정보 반환
        
        return user # user는 {'Student_ID': '...', 'Pw': '...'} 또는 None
        
    except Exception as e:
        print(f"유저 조회 오류: {e}")
        return None
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()