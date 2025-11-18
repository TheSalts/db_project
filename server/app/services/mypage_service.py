# app/services/mypage_service.py

import pymysql
import bcrypt
from app.utils.db import get_db_connection

def get_user_info(student_id):
    """(마이페이지) 내 정보 조회"""
    conn = None
    cursor = None
    
    # 비밀번호(Pw)를 제외한 모든 정보 조회
    sql = """
        SELECT Student_ID, Login_ID, Name, phone_num, Email, Role 
        FROM Student 
        WHERE Student_ID = %s
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (student_id,))
        user_info = cursor.fetchone()
        return user_info
        
    except Exception as e:
        print(f"내 정보 조회 오류: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_user_info(student_id, data):
    """(마이페이지) 내 정보 수정"""
    conn = None
    cursor = None
    
    # 1. SQL 쿼리 동적 생성 (바꾸려는 값만 UPDATE)
    # SET 절에 들어갈 필드와 값을 리스트로 준비
    fields_to_update = []
    values = []

    if 'Name' in data:
        fields_to_update.append("Name = %s")
        values.append(data['Name'])
    if 'phone_num' in data:
        fields_to_update.append("phone_num = %s")
        values.append(data['phone_num'])
    if 'Email' in data:
        fields_to_update.append("Email = %s")
        values.append(data['Email'])
    
    # 2. 비밀번호(Pw) 변경이 포함된 경우 (bcrypt 해시 처리)
    if 'Pw' in data and data['Pw']: # 비어있지 않은 Pw 값이 온 경우
        password = data['Pw'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        fields_to_update.append("Pw = %s")
        values.append(hashed_password)

    # 바꿀 내용이 없으면 함수 종료
    if not fields_to_update:
        return True, "변경할 내용이 없습니다."

    # 3. 쿼리 실행
    sql = f"UPDATE Student SET {', '.join(fields_to_update)} WHERE Student_ID = %s"
    values.append(student_id) # WHERE 절에 들어갈 student_id 추가
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, tuple(values))
        conn.commit()
        
        # 변경된 행이 0개 초과면 성공
        if cursor.rowcount > 0:
            return True, "정보가 성공적으로 수정되었습니다."
        else:
            return True, "변경된 정보가 없습니다." # 에러는 아니지만 변경 안됨

    except pymysql.err.IntegrityError as e:
        # 이메일 중복 체크 (UK_Email)
        if e.args[0] == 1062 and 'UK_Email' in e.args[1]:
            return False, "이미 사용 중인 이메일입니다."
        return False, "데이터베이스 오류"
    except Exception as e:
        print(f"내 정보 수정 오류: {e}")
        return False, "서버 오류 발생"
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_my_applications(student_id):
    """(마이페이지) 내 가입 신청 현황 조회"""
    conn = None
    cursor = None
    
    # Club 테이블과 JOIN해서 동아리 이름 가져옴
    sql = """
        SELECT 
            a.Application_ID,
            a.Club_ID,
            c.Club_name,
            a.Self_Introduction,
            a.Application_Date,
            a.Status
        FROM Apply a
        JOIN Club c ON a.Club_ID = c.Club_ID
        WHERE a.Student_ID = %s
        ORDER BY a.Application_Date DESC
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (student_id,))
        applications = cursor.fetchall()
        return applications
        
    except Exception as e:
        print(f"내 신청 현황 조회 오류: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_my_clubs(student_id):
    """(마이페이지) 내가 가입한 동아리 목록 조회"""
    conn = None
    cursor = None
    
    # Belong 테이블과 Club 테이블을 JOIN
    sql = """
        SELECT 
            b.Membership_ID,
            b.Club_ID,
            c.Club_name,
            c.Category,
            b.Position
        FROM Belong b
        JOIN Club c ON b.Club_ID = c.Club_ID
        WHERE b.Student_ID = %s
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (student_id,))
        clubs = cursor.fetchall()
        return clubs
        
    except Exception as e:
        print(f"내 동아리 목록 조회 오류: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()